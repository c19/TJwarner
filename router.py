#!/usr/bin/env python
# coding=utf-8
#    URL Router for TJwarner
#    C19<classone2010@gmail.com>

import web
from database import Room
from monitor  import monitor
from sendmail import sendmail
import pdb

from uwsgidecorators import *

urls = (
        '/', 'index',  #only for testing
        '/submit', 'submit',
        '/success', 'success',
        '/fail', 'fail',
        )

@cron(40,-1,-1,-1,-1)
def check_all(*arg, **kwarg):
    print("check_all")
    monitor.check_all()
    print("check_all Done")

class index:
    def GET(self):
        web.header('Content-Type', 'text/html; charset=UTF-8')
        return open('index.html').read()

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
                     u'电量低于{0}时将发送提示邮件到此邮箱。'.format(room.threshold)
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
if __name__ == "__main__":
    app.run()
else:
    application = app.wsgifunc()
