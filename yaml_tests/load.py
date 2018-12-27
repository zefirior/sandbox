import yaml as y
from pprint import pprint


with open("data.yml", 'r') as yf:
    data = y.load(yf)
    pprint(data)
