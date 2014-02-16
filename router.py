#!/usr/bin/env python
# coding=utf-8
#    URL Router for TJwarner
#    C19<classone2010@gmail.com>

from hashlib import sha256
from random  import random
from datetime import datetime,timedelta
import json
import pdb

import web
web.config.debug = False
web.config.session_parameters['cookie_name'] = 'session'
web.config.session_parameters['cookie_domain'] = None
web.config.session_parameters['timeout'] = 86400 #24 * 60 * 60, # 24 hours   in seconds
web.config.session_parameters['ignore_expiry'] = False
web.config.session_parameters['ignore_change_ip'] = False
web.config.session_parameters['expired_message'] = 'Session expired'

from database import Room,Auth
from monitor  import monitor
from sendmail import sendmail
from spooler  import spool
try:
    from uwsgidecorators import *
    import uwsgi
except ImportError as err:
    print(err)
else:
    @cron(40,-1,-1,-1,-1)
    def check_all(*arg, **kwarg):
        print("check_all")
        monitor.check_all()
        print("check_all Done")
    #@spool
    #def spooler(kwargs):
    #    print(kwargs)


def rnd_id(string):
    return sha256(str(random()) + string).hexdigest()

def setting_url(addrindex):
    rndid = rnd_id(addrindex)
    auth  = Auth({'rndid': rndid,
                  'addrindex': addrindex})
    auth.save()
    return "http://tjwarner.caoyijun.com/setting/{0}".format(rndid)

urls = (
        '/', 'index',  #only for testing
        '/submit', 'submit',
        '/success', 'success',
        '/fail', 'fail',
        '/setting/([a-z0-9]{64})', 'setting',
        )



class setting:
    def GET(self, rndid):
        cursor = Auth.find({'rndid': rndid})
        if cursor.count() == 0:
            return '嗯，我不记得我有给过你这个链接诶。'
        auth = cursor.next()
        #if auth.expires  + timedelta(days=7) > datetime.utcnow():
        #    return '唔。那是我至少7天前给你发的，不算。'
        session.addrindex = auth.addrindex
        return open('static/setting.html').read()
    def POST(self, rndid):
        if not session.addrindex: return '嘿，你谁？session都清掉了？'
        def purge(inputs):
            Auth.collection.remove({'addrindex': session.addrindex})
            Room.collection.remove({'addrindex': session.addrindex})
            addr = session.addrindex
            session.kill()
            return u'{0}所有信息已清除。'.format(addr)
        def delay(inputs):
            days = int(inputs['days'])
            room = Room.find_one({'addrindex': session.addrindex})
            if not room: return '找不到房间信息，已经删了？'
            delay = datetime.utcnow() + timedelta(days=days)
            Room.find_and_modify({'addrindex': session.addrindex}, 
                                 {'$set':{'last_check': delay}})
            return '到{0}前不会发送提醒邮件。'.format(delay)
        inputs = web.input()
        switch = {'purge': purge,
                  'delay': delay,}
        try:
            return switch[inputs['action']](inputs)
        except Exception, e:
            return '你想干嘛'
class index:
    def GET(self):
        print(roomstr)
        pdb.set_trace()
        spool(roomstr)
        web.header('Content-Type', 'text/html; charset=UTF-8')
        return open('static/index.html').read()

class success:
    def GET(self):
        web.header('Content-Type', 'text/html; charset=UTF-8')
        return u'请查看邮件'.encode('utf-8')

class fail:
    def GET(self):
        web.header('Content-Type', 'text/html; charset=UTF-8')
        return u'出错了，如果你想，可以发邮件到classone2010@gmail.com抱怨。'.encode('utf-8')

class submit:
    def POST(self):
        room = self.check(web.input())
        print(room)
        try:
            yield("checking ...")
            balance = monitor.check_balance(room)
            yield("sending mail...")
            sendmail(room.email, u'{0}{1}电量剩余{2} Kwh'.format(room.addr['BuildingDown'], room.addr['RoomnameText'], balance),
                     u'电量低于{0}时将发送提示邮件到此邮箱。\n<a href="{1}">点此设置开学后再提醒或清除账号</a>'.format(room.threshold, setting_url(room.addrindex))
                    )
            room.save()
            yield("done, check your email.")
        except Exception, e:
            web.SeeOther('/fail')
            return
        web.SeeOther('/success')
    def check(self,inputs):
        try:
            args = (inputs['building'][:33], inputs['room'][:33], inputs['district'][:33])
            args = [arg if isinstance(arg,unicode) else arg.decode('utf-8') for arg in args]
            room = { "threshold" : int(inputs['threshold']),
                     "addr" : { "BuildingDown" : args[0],
                                "RoomnameText" : args[1],
                                "DistrictDown" : args[2],
                                },
                     "email" : inputs['email'][:120] }
            room = Room(room)
            return room
        except Exception, e:
            web.SeeOther('/fail')

app = web.application(urls, globals())
session = web.session.Session(app, web.session.DiskStore('sessions'), initializer={'addrindex': None})
myroom = { "threshold" : 10, "addrindex" : u"322四平校区西南八楼    ",
           "addr" : { "BuildingDown" : u"西南八楼    ", u"RoomnameText" : "322", "DistrictDown" : u"四平校区" },
           "email" : "classone2010@gmail.com" }
#myroom = Room(myroom)
roomstr = json.dumps(myroom)

if __name__ == "__main__":
    app.run()
else:
    application = app.wsgifunc()