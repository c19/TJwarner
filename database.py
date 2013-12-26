#!/usr/bin/env python
# coding=utf-8
#        ORM
#        C19<classone2010@gmail.com>

#from pymongo import MongoClient
from copy import deepcopy

from mongokit import *
from datetime import datetime

import pdb

connection = Connection()

@connection.register
class Room(Document):
    __database__ = 'TJrooms'
    __collection__ = 'rooms'
    use_dot_notation = True
    structure = {
                 'addr':           dict,
                 'threshold':      int,
                 'email':          basestring,
                 'addrindex':      basestring,
                 'balance':        float,
                 'last_check':     datetime,
                }
    indexes = [{
                'fields': 'addrindex',
                'unique': True,
                }]
    required_fields = ['addr', 'email', 'threshold']
    default_values  = {'threshold': 10}
    #validators = {
    #              'addr': lambda addr: ''.join(sorted(addr.values()))
    #              }
    #def __init__(self, *arg, **kwarg):
    #    super(Room, self).__init__(self, *arg, **kwarg)
    #    self['addrindex'] = ''.join(sorted(self['addr'].values()))
    def add_addrindex(self):
        self['addrindex'] = ''.join(sorted(self['addr'].values()))
    def save(self, key=None):
        self.add_addrindex()
        #self.validate()
        if not key: key = {'addrindex': self['addrindex']}
        self.collection.update(key, self, upsert=True, check_keys=False, safe=False, manipulate=False)
Room = connection.Room
