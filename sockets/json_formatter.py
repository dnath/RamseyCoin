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

#type 0 getseed request data is None
#type 1 saveseed request data is counter example
#type 2 takeseed response data is the largest counterexample we have
class message:
	def __init__(self, type, data=None):
		if data != None:
			self.type = type
			self.data = data
		else :
			dict = json.loads(type)
			self.type = int(dict["type"])
			self.data = dict["data"]
	def get_json(self):
		dict = {}
		dict["type"] = self.type
		if(self.data != None):
			dict["data"] = self.data
		else:
			dict["data"] = ""
		return json.dumps(dict)