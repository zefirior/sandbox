import attr
from decimal import Decimal

from utils import lstr2idate, decimal_if_not_empty


@attr.s(slots=True)
class Cs:
    accserv_id = attr.ib(converter=int)
    from_date = attr.ib(converter=lstr2idate)
    to_date = attr.ib(converter=lstr2idate)
    objlist = attr.ib(init=False, default=None)
    servable = attr.ib(init=False, default=None)
    adesc = attr.ib(init=False, default=None)
    fdesc = attr.ib(init=False, default=None)
    hdesc = attr.ib(init=False, default=None)
    haccserv = attr.ib(init=False, default=None)
    tariff = attr.ib(init=False, default=None)

    def construct_key(self, keys):
        return tuple(getattr(self.objlist, attr) for attr in keys)



@attr.s(slots=True)
class ObjList:
    accserv_id = attr.ib(converter=int)
    accserv_obj_id = attr.ib(converter=int)
    account_id = attr.ib(converter=int)
    account_obj_id = attr.ib(converter=int)
    house_id = attr.ib(converter=int)
    house_obj_id = attr.ib(converter=int)
    agent_id = attr.ib(converter=int)
    agent_obj_id = attr.ib(converter=int)
    reseller_id = attr.ib(converter=int)
    reseller_obj_id = attr.ib(converter=int)
    provider_id = attr.ib(converter=int)
    provider_obj_id = attr.ib(converter=int)
    resprov_id = attr.ib(converter=int)
    resprov_obj_id = attr.ib(converter=int)
    service_id = attr.ib(converter=int)
    acctype_id = attr.ib(converter=int)
    flat_id = attr.ib(converter=int)


@attr.s(slots=True)
class HAccServ:
    accserv_id = attr.ib(converter=int)
    haccserv_stype = attr.ib()
    haccserv_fnds = attr.ib(converter=Decimal)
    from_date = attr.ib(converter=lstr2idate)
    to_date = attr.ib(converter=lstr2idate)


@attr.s(slots=True)
class Servable:
    service_id = attr.ib(converter=int)
    provider_id = attr.ib(converter=int)
    from_date = attr.ib(converter=lstr2idate)
    to_date = attr.ib(converter=lstr2idate)


@attr.s(slots=True)
class HDesc:
    house_id = attr.ib(converter=int)
    hdesc_fbroken = attr.ib(converter=lambda s: int(s) if s else None)
    from_date = attr.ib(converter=lstr2idate)
    to_date = attr.ib(converter=lstr2idate)


@attr.s(slots=True)
class ObjLinkAccOg:
    account_id = attr.ib(converter=int)
    account_obj_id = attr.ib(converter=int)
    objgroup_id = attr.ib(converter=int)
    fondobj_id = attr.ib(converter=int)
    from_date = attr.ib(converter=lstr2idate)
    to_date = attr.ib(converter=lstr2idate)


@attr.s(slots=True)
class ObjLinkHHg:
    account_id = attr.ib(converter=int)
    account_obj_id = attr.ib(converter=int)
    objgroup_id = attr.ib(converter=int)
    fondobj_id = attr.ib(converter=int)
    from_date = attr.ib(converter=lstr2idate)
    to_date = attr.ib(converter=lstr2idate)


@attr.s(slots=True)
class ADesc:
    account_id = attr.ib(converter=int)
    adesc_s0 = attr.ib(converter=decimal_if_not_empty)
    adesc_sl = attr.ib(converter=decimal_if_not_empty)
    adesc_sh = attr.ib(converter=decimal_if_not_empty)
    adesc_se = attr.ib(converter=decimal_if_not_empty)
    adesc_sp = attr.ib(converter=decimal_if_not_empty)
    adesc_sd = attr.ib(converter=decimal_if_not_empty)
    from_date = attr.ib(converter=lstr2idate)
    to_date = attr.ib(converter=lstr2idate)


@attr.s(slots=True)
class FDesc:
    flat_id = attr.ib(converter=int)
    fcat_id = attr.ib(converter=int)
    from_date = attr.ib(converter=lstr2idate)
    to_date = attr.ib(converter=lstr2idate)


@attr.s(slots=True)
class ATariff:
    accserv_id = attr.ib(converter=int)
    accserv_obj_id = attr.ib(converter=int)
    tariff_value = attr.ib(converter=Decimal)
    from_date = attr.ib(converter=lstr2idate)
    to_date = attr.ib(converter=lstr2idate)


@attr.s(slots=True)
class GTariff:
    service_id = attr.ib(converter=int)
    agent_id = attr.ib(converter=int)
    tariff_value = attr.ib(converter=Decimal)
    from_date = attr.ib(converter=lstr2idate)
    to_date = attr.ib(converter=lstr2idate)


@attr.s(slots=True)
class HTariff:
    house_id = attr.ib(converter=int)
    service_id = attr.ib(converter=int)
    resprov_id = attr.ib(converter=int)
    resprov_obj_id = attr.ib(converter=int)
    tariff_value = attr.ib(converter=Decimal)
    from_date = attr.ib(converter=lstr2idate)
    to_date = attr.ib(converter=lstr2idate)


@attr.s(slots=True)
class RTariff:
    service_id = attr.ib(converter=int)
    reseller_id = attr.ib(converter=int)
    reseller_obj_id = attr.ib(converter=int)
    tariff_value = attr.ib(converter=Decimal)
    from_date = attr.ib(converter=lstr2idate)
    to_date = attr.ib(converter=lstr2idate)
