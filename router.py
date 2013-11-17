#!/usr/bin/env python
# coding=utf-8
#    URL Router for TJwarner
#    C19<classone2010@gmail.com>

import web
from database import DB,Room
from monitor  import monitor
from sendmail import sendmail
import pdb

urls = (
        '/', 'index',  #only for testing
        '/submit', 'submit',
        )

class index:
    def GET(self):
        return open('index.html').read()

class submit:
    """room = Room(('四平校区','西南八楼    ','322'),email='classone2010@gmail.com')"""
    def POST(self):
        room = self.check(web.input())
        print(room)
        try:
            #pdb.set_trace()
            fee = monitor.get_fee(room)
            sendmail(room.email, '{0}{1}电量剩余{2} Kwh'.format(room.addr['BuildingDown'], room.addr['RoomnameText'], fee),
                     '电量低于{0}时将发送提示邮件到此邮箱。'.format(room.threshold)
                    )
            room.save()
        except Exception, e:
            raise e
        web.SeeOther('/success')
    def check(self,inputs):
        #pdb.set_trace()
        #try:
            arg1 = inputs['district'][:33].encode('utf-8')
            arg2 = inputs['building'][:33].encode('utf-8')
            arg3 = inputs['room'][:33].encode('utf-8')
            email= inputs['email'][:120]
            threshold = int(inputs['threshold'])
            room = Room((arg1,arg2,arg3), threshold=threshold, email=email)
            return room
        #except Exception, e:
        #    web.SeeOther('/fail')

app = web.application(urls, globals())
if __name__ == "__main__":
    app.run()
else:
    application = app.wsgifunc()