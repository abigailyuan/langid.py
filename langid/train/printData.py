import json
from collections import defaultdict as dd
from pprint import pprint


import collections

with open('dev.json') as json_data:
    data = json.load(json_data)
    #print(data)
    langDict = dd(int)
    for item in data:
        lang = item.get("lang")
        langDict[lang] += 1
    print(langDict) 
