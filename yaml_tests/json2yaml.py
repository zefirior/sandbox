import json
import yaml as y
from pprint import pprint

with open("dump.yml", "w") as yf:
    with open("main_calc.json", "r") as jf:
        data = json.load(jf)
        pprint(data)
        y.dump(data, yf)
