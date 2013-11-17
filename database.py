#!/usr/bin/env python
# coding=utf-8
#        ORM
#        C19<classone2010@gmail.com>

from pymongo import MongoClient
from copy import deepcopy

import pdb

class MyDict(dict):
    def __getattr__(self, key):
        return self[key]
    def __setattr__(self, key, value):
        if isinstance(value,dict):
            self[key] = MyDict(value)
        else:
            self[key] = value

class DBdict(MyDict):
    def __init__(self,*arg,**kwarg):
        MyDict.__init__(self)
        s = deepcopy(self.structure)
        self.update(s)
        if len(kwarg):self.update(dict(**kwarg))
    def save(self):
        DB.save(self)

class Room(DBdict):
    """{'threshold':10,'addr':{'DistrictDown':u'四平校区', 'BuildingDown':u'西南八楼    ','RoomnameText':u'322'}}"""
    colname = 'rooms'
    def __init__(self, *arg, **kwarg):
        super(Room, self).__init__(self, *arg, **kwarg)
        if arg and len(*arg)==3: 
            self.update({'addr': dict(zip(('DistrictDown','BuildingDown','RoomnameText'),*arg))})
        self['addrindex'] = ''.join(sorted(self['addr'].values()))
    structure = {
                 'addr': {},
                 'threshold': 10,
                 'email':  [],
                 'addrindex':   '',
                }

class DB(object):
    indexs = {'rooms':[{'key':[('addrindex',1)], 'unique':True}]}
    conn = MongoClient()
    @classmethod
    def connect(cls):
        cls.db = cls.conn['TJrooms']
        for col in cls.indexs.keys():
            try:
                cls.db.create_collection(col,autoIndexId = False)
            except Exception,e:
                pass
        cls.cols = {colname:cls.db[colname] for colname in cls.indexs.keys()}
        cls.ensure_index()
    @classmethod
    def ensure_index(cls):
        for colname,indexes in cls.indexs.items():
            for index in indexes:
                key = index['key']
                kwarg = deepcopy(index)
                del kwarg['key']
                cls.cols[colname].ensure_index(key,**kwarg)
    @classmethod
    def save(cls,obj,key=None):
        key = {'addr':obj.addrindex} if key is None else key
        #update(self, spec, document, upsert=False, manipulate=False, safe=None, multi=False, check_keys=True, **kwargs)
        cls.cols[obj.colname].update(key, obj, upsert=True, check_keys=False, safe=False, manipulate=False)
DB.connect()