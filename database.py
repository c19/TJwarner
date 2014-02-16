#!/usr/bin/env python
# coding=utf-8
#        ORM
#        C19<classone2010@gmail.com>

#from pymongo import MongoClient
from copy import deepcopy

from mongokit import *
from datetime import datetime,timedelta

import pdb

connection = Connection()

@connection.register
class Auth(Document):
    __database__   = 'TJrooms'
    __collection__ = 'auths'
    use_dot_notation = True
    structure = {
                 'rndid':     basestring,
                 'addrindex': basestring,
                 'expires':   datetime,
                 }
    indexes = [{
                'fields': ['rndid', 'addrindex'],
                'unique': True,
                }]
    required_fields = ['rndid', 'addrindex']
    default_values  = {'expires': datetime.utcnow()}
    def save(self):
        self.collection.update({'addrindex': self['addrindex']}, self, upsert=True, check_keys=False, safe=False, manipulate=False)

@connection.register
class Room(Document):
    __database__     = 'TJrooms'
    __collection__   = 'rooms'
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
        self['addrindex'] = ''.join([room.addr['DistrictDown'],room.addr['BuildingDown'],room.addr['RoomnameText']])
    def save(self):
        self.add_addrindex()
        key = {'addrindex': self['addrindex']}
        self.collection.update(key, self, upsert=True, check_keys=False, safe=False, manipulate=False)
Room = connection.Room
Auth = connection.Auth