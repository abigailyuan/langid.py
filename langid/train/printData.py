import json
from pprint import pprint

import collections

with open('dev.json') as json_data:
	data = json.load(json_data)
	print(data)

