import csv
from copy import copy
from enum import Enum
from collections import Iterable

import models as m
from utils import timeit, make_index


def is_cross(interval1, interval2):
    return interval1.from_date < interval2.to_date and interval2.from_date < interval1.to_date


def join_interval(main_interval, list_interval, mount_dot):
    result = []
    count = 0

    for interval in list_interval:
        if is_cross(main_interval, interval):
            count += 1
            res = main_interval if count == 1 else copy(main_interval)
            res.from_date = max(main_interval.from_date, interval.from_date)
            res.to_date = min(main_interval.to_date, interval.to_date)
            setattr(res, mount_dot, interval)
            join_result.append(res)
    return result


def link_i_chank_to_interval(i_chank, interval):
    i_chank = iter(sorted(i_chank))
    interval = iter(sorted(interval, key=lambda i: i.from_date))

    i_map = []
    cur_chank, cur_i = next(i_chank, None), next(interval, None)
    while True:

        if cur_chank is None:
            break

        if cur_i is not None and cur_i.to_date <= cur_chank[0]:
            cur_i = next(interval, None)
            continue

        if cur_i is None or cur_chank[1] <= cur_i.from_date:
            i_map.append((cur_chank, None))
            cur_chank = next(i_chank, None)
            continue

        i_map.append((cur_chank, cur_i))
        cur_chank = next(i_chank, None)

    return i_map


def left_join_interval(main_interval, list_interval, mount):
    if not list_interval:
        yield main_interval
        return

    if len(list_interval) > 1:
        list_interval = sorted(list_interval, key=lambda i: i.from_date)

    dots = {main_interval.from_date, main_interval.to_date}
    for i in list_interval:
        dots.add(i.from_date)
        dots.add(i.to_date)

    dots = sorted(dots)
    dots = [dot for dot in dots if main_interval.from_date <= dot <= main_interval.to_date]

    # if len(dots) == 2:
    #     yield main_interval
    #     return

    i_map = link_i_chank_to_interval(
        zip(dots[:-1], dots[1:]),
        list_interval
    )

    for chank, interval in i_map:
        res_i = copy(main_interval)
        res_i.from_date = chank[0]
        res_i.to_date = chank[1]
        if interval:
            setattr(res_i, mount, interval)
        yield res_i


class Interval:
    def __init__(self, from_date, to_date):
        self.from_date = from_date
        self.to_date = to_date
        self.mount = None

    def __repr__(self):
        return '<Interval ({}, {}, {})>'.format(self.from_date, self.to_date, self.mount)


class Tariffer:

    def __init__(self):
        self.tariff = {}
        self.index = {}
        self.key = {}

    def register_tariff(self, label, tariff, key):
        self.tariff[label] = tariff
        index = make_index(tariff, key)
        self.index[label] = index
        self.key[label] = key

    def create_iterator(self, cs):
        return TarifferIterator(self, cs)


class TarifferIterator(Iterable):
    def __init__(self, store: Tariffer, cs: m.Cs):
        self.store = store
        self.cs = cs
        self.tar_type = iter([Label.atariff, Label.htariff, Label.rtariff, Label.gtariff])
        self.cur_tar_type = None
        self.cur_tar_list = None
        self.next_type()
        self.pos = 0

    def __iter__(self):
        return self

    def __next__(self):
        while True:
            if self.pos >= len(self.cur_tar_list):
                self.next_type()
            else:
                break

        self.pos += 1
        return self.cur_tar_list[self.pos - 1]

    def next_type(self):
        self.cur_tar_type = next(self.tar_type)

        keys = self.store.key[self.cur_tar_type]
        key = self.cs.construct_key(keys)
        self.cur_tar_list = self.store.index[self.cur_tar_type][key]
        self.pos = 0


if __name__ == '__main__':
    class Label(Enum):
        cslist = 1
        objlist = 2
        haccserv = 3
        servable = 4
        hdesc = 5
        adesc = 6
        fdesc = 7
        objlink_acc_og = 8
        objlink_h_hg = 9
        atariff = 10
        gtariff = 11
        htariff = 12
        rtariff = 13


    source = [
        # name, model, file
        (Label.cslist, m.Cs, 'cs_list2'),
        (Label.objlist, m.ObjList, 'obj_list'),
        (Label.haccserv, m.HAccServ, 'haccserv'),
        (Label.servable, m.Servable, 'servable'),
        (Label.hdesc, m.HDesc, 'hdesc'),
        (Label.adesc, m.ADesc, 'adesc'),
        (Label.fdesc, m.FDesc, 'fdesc'),
        (Label.objlink_acc_og, m.ObjLinkAccOg, 'objlink_acc_og'),
        (Label.objlink_h_hg, m.ObjLinkHHg, 'objlink_h_hg'),
        (Label.atariff, m.ATariff, 'atariff'),
        (Label.gtariff, m.GTariff, 'gtariff'),
        (Label.htariff, m.HTariff, 'htariff'),
        (Label.rtariff, m.RTariff, 'rtariff'),
    ]

    with timeit('all'):
        with timeit('generate'):
            data = {}
            for name, model, file_name in source:

                print(name)
                with open('/home/liinda/tmp/mule_csv/pull/' + file_name, 'r') as csvf:
                    reader = csv.reader(csvf, delimiter=';')
                    source_data = []
                    for row in reader:
                        source_data.append(model(*row))
                    data[name] = source_data
                    if source_data:
                        print(len(source_data))
                        print(source_data[0])
                        print()

        with timeit('objlist'):

            index = make_index(data[Label.objlist], ['accserv_id'])

            for cs in data[Label.cslist]:
                if (cs.accserv_id,) in index:
                    cs.objlist = index[(cs.accserv_id,)][0]
            data[Label.cslist] = [_ for _ in data[Label.cslist] if _.objlist]

        with timeit('servable'):

            index = make_index(data[Label.servable], ['service_id', 'provider_id'])

            join_result = []
            for cs in data[Label.cslist]:
                servables = index[(cs.objlist.service_id, cs.objlist.provider_id)]
                join_result += join_interval(cs, servables, 'servable')
            data[Label.cslist] = join_result

            del join_result, index

        with timeit('adesc'):

            index = make_index(data[Label.adesc], ['account_id'])

            join_result = []
            for cs in data[Label.cslist]:
                adesc = index[(cs.objlist.account_id,)]
                join_result += join_interval(cs, adesc, 'adesc')
            data[Label.cslist] = join_result

            del join_result, index

        with timeit('fdesc'):

            index = make_index(data[Label.fdesc], ['flat_id'])

            join_result = []
            for cs in data[Label.cslist]:
                fdesc = index[(cs.objlist.flat_id,)]
                join_result += join_interval(cs, fdesc, 'fdesc')
            data[Label.cslist] = join_result

            del join_result, index

        with timeit('hdesc'):

            index = make_index(data[Label.hdesc], ['house_id'])

            join_result = []
            for cs in data[Label.cslist]:
                hdesc = index[(cs.objlist.house_id,)]
                join_result += join_interval(cs, hdesc, 'hdesc')

            data[Label.cslist] = join_result

            del join_result, index

        print(data[Label.cslist][1])
        print(data[Label.cslist][2])

        with timeit('tariff'):
            tar_store = Tariffer()
            tar_store.register_tariff(Label.atariff, data[Label.atariff], ['accserv_id'])
            tar_store.register_tariff(Label.htariff, data[Label.htariff], ['house_id', 'service_id', 'resprov_obj_id'])
            tar_store.register_tariff(Label.rtariff, data[Label.rtariff], ['service_id', 'reseller_obj_id'])
            tar_store.register_tariff(Label.gtariff, data[Label.gtariff], ['service_id'])

            result = []
            for cs in data[Label.cslist]:
                tar_iter = tar_store.create_iterator(cs)
                for_find = [cs]
                while True:
                    tariff = next(tar_iter, None)

                    if tariff is None or not for_find:
                        break

                    unuse = []
                    for cs in for_find:
                        intervals = list(left_join_interval(cs, [tariff], 'tariff'))
                        result += [_ for _ in intervals if _.tariff]
                        unuse += [_ for _ in intervals if _.tariff is None]
                    for_find = unuse

        print(len(result))
        print(result[6])
