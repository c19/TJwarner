#!/usr/bin/env python
# coding=utf-8
#    URL Router for TJwarner
#    C19<classone2010@gmail.com>

import web
from database import Room
from monitor  import monitor
from sendmail import sendmail
import pdb

urls = (
        '/', 'index',  #only for testing
        '/submit', 'submit',
        '/success', 'success',
        '/fail', 'fail',
        )

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
        return u'出错了，我也不知道怎么回事，如果你想，可以发邮件到classone2010@gmail.com抱怨。'.encode('utf-8')

class submit:
    def POST(self):
        room = self.check(web.input())
        print(room)
        try:
            balance = monitor.get_balance(room)
            sendmail(room.email, '{0}{1}电量剩余{2} Kwh'.format(room.addr['BuildingDown'], room.addr['RoomnameText'], balance),
                     '电量低于{0}时将发送提示邮件到此邮箱。'.format(room.threshold)
                    )
            room.save()
        except Exception, e:
            web.SeeOther('/fail')
        web.SeeOther('/success')
    def check(self,inputs):
        
        try:
            room = { "threshold" : int(inputs['threshold']),
                     "addr" : { "BuildingDown" : inputs['building'][:33].encode('utf-8'),
                                "RoomnameText" : inputs['room'][:33].encode('utf-8'),
                                "DistrictDown" : inputs['district'][:33].encode('utf-8')
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