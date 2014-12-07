#!/usr/bin/python           
import json
from common import *

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



class Message:
  @staticmethod
  def decode(encoded_message):
    json_obj = json.loads(encoded_message)
    msg_type = int(json_obj["type"])
    
    if json_obj["data_size"] == '' or json_obj["data_size"] is None:
      data_size = 0
    else:
      data_size = int(json_obj["data_size"])
    
    return Message(msg_type, data=json_obj["data"], data_size=data_size,
                              Id=json_obj["Id"], IP=json_obj["IP"], hostname=json_obj["hostname"], Port=json_obj["Port"],
                              client_dict=json_obj["client_dict"])

  def __init__(self, type, data='', data_size='', Id='', IP='', hostname='', Port='', client_dict=''):
    self.type = type
    self.data = data
    self.data_size = data_size
    self.Id = Id
    self.IP = IP
    self.hostname = hostname
    self.Port = Port
    self.client_dict = client_dict
    
   #  else:
      # dict = json.loads(type)
      # self.type = int(dict["type"])
      # self.data = dict["data"]
      # self.Id = dict["Id"]
      # self.IP = dict["IP"]
      # self.Port = dict["Port"]

  def get_json(self):
    json_obj = {}
    json_obj["type"] = self.type
    json_obj["data"] = self.data
    json_obj["data_size"] = self.data_size
    json_obj["Id"] = self.Id
    json_obj["IP"] = self.IP
    json_obj["hostname"] = self.hostname
    json_obj["Port"] = self.Port
    json_obj["client_dict"] = self.client_dict
    
    return json.dumps(json_obj)

  def __str__(self):
    return self.get_json()

if __name__ == '__main__':
  m = Message(GET_SEED, data='100100101', data_size=3, Id='121', IP='127.0.1.1', hostname='local', Port=12443, client_dict={'d':'1'})
  print m

  msg_string = str(m)
  m1 = Message.decode(msg_string)
  print m1
