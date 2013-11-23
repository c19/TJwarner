#!/usr/bin/env python
# coding=utf-8
#   Tongji University electricity charge low pre warning
#   C19<classone2010@gmail.com>

from urllib2 import HTTPError
from urllib  import urlencode
from webdumper import Webdumper
from sendmail  import sendmail
#from lxml import etree
import re
from database import Room
from datetime import datetime as time
import datetime
import pdb

class Monitor(Webdumper):
    """Monitor for 'http://nyglzx.tongji.edu.cn/web/datastat.aspx'"""
    def __init__(self, *arg, **kwarg):
        self.url = 'http://nyglzx.tongji.edu.cn/web/datastat.aspx'
        self.raw = """__EVENTTARGET=&__EVENTARGUMENT=&__LASTFOCUS=&__VIEWSTATE=%s&__EVENTVALIDATION=%s
                DistrictDown={0}&BuildingDown={1}&RoomnameText={2}&Submit=查询"""
        self.validers = {'__EVENTTARGET':None,
                         '__EVENTARGUMENT':None,
                         '__LASTFOCUS':None,
                         '__VIEWSTATE':None,
                         '__EVENTVALIDATION':None,
                        }
        super(Monitor, self).__init__(self, *arg, **kwarg)
        self.get(self.url)
        self.get_validers()
    def get(self, url, data=None):
        html = super(Monitor, self).get(url, data)
        self.get_validers()
        return html
    def check_all(self, delay=6):
        cursor = Room.find()
        cursor = cursor.batch_size(5)
        for room in cursor:
            if room.has_key('last_check') and :
                if time.utcnow() - room.last_check >= datetime.timedelta(hours=delay):
                    self.check_balance(room)
            else:
                self.check_balance(room)
    def check_balance(self,rooms):
        if isinstance(rooms,list):
            for room in rooms:
                    self.check_balance(room)
        else:
            self.get(self.url)
            data = urlencode(dict(self.validers.items() + [('DistrictDown',rooms.addr['DistrictDown'].encode('utf-8'))]))
            #pdb.set_trace()
            self.get(self.url, data)
            #try:
            #sorry for the ugly code, the page is incredibly awful and strange,
            #it has to post a long nonsence __VIEWSTATE and html was full of 
            #tables, somehow lxml.etree coudn't parse correctly.
            #en, urlencode only accepts utf8, and i'm too lazy to change the database.
            data = urlencode(dict(self.validers.items() + zip(rooms.addr.keys(),[a.encode('utf-8') for a in rooms.addr.values()]) + [('Submit','查询')]))
            #data = data.replace('=','%3d').replace('&','%26')  #quick fix, sorry for this but the server only accept this way,at the post.
            #print(data)
            html = self.get(self.url, data)
            n    = html.find('剩余电量（kWh）</th>')
            table= html[n:n+400]
            cells= re.findall(re.compile('<td>(.*?)</td>'),table)
            balance = cells[3]
            balance = float(balance)
            if balance < rooms.threshold:
                sendmail(rooms.email, '{0}{1}快没电费啦！！！'.format(rooms.addr['BuildingDown'],rooms.addr['RoomnameText']), '还剩{0}Kwh =w='.format(balance))
            rooms['balance'] = balance
            rooms['last_check'] = time.utcnow()
            rooms.save()
            return balance
            '''except HTTPError, e:
                if e.getcode() == 500:
                    self.get_validers()
                else:
                    raise e'''
    def _get_valider(self, id):
        ptn = re.compile('id="{0}" value="(.*)"'.format(id))
        valider = re.findall(ptn, self.html)
        if len(valider):
            return valider[0]
        else:
            raise Exception("Can't get {0}".format(id))
    def get_validers(self):
        #html = self.get(self.url)
        self.validers = {valider: self._get_valider(valider) for valider in self.validers.keys()}

monitor = Monitor()
"""myroom = { "threshold" : 10, "addrindex" : u"322四平校区西南八楼    ",
           "addr" : { "BuildingDown" : u"西南八楼    ", u"RoomnameText" : "322", "DistrictDown" : u"四平校区" },
           "email" : "classone2010@gmail.com" }
myroom = Room(myroom)
"""
if __name__ == '__main__':
    monitor.check_all(0)