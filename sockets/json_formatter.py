#!/usr/bin/python           
import json					# Import json module

'''
Counter Example class
We have 2 constructors either with data and size or with json objects
We have also a function to return the corresponding json with this object
'''
class CounterExample:
	def __init__(self, data, size=None):
		if size != None:
			self.size = size
			self.data = data
		else :
			dict = json.loads(data)
			self.size = int(dict["size"])
			self.data = dict["data"]	
	def get_json(self):
		dict = {}
		dict["data"] = self.data
		return json.dumps(dict)


