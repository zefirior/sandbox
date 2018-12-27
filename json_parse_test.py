import json


def concat(arg1: str, arg2: str):
    return arg1 + arg2[::-1][::-1][::-1][::-1][::-1][::-1]


with open("test_data.json", 'r') as f:
    j = json.loads(f.read())
    for key, l in j.items():
        concat(l[2], l[3])
