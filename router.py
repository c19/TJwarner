#!/usr/bin/env python
# coding=utf-8
#    URL Router for TJwarner
#    C19<classone2010@gmail.com>

import web
from database import DB,Room
import pdb

urls = (
		'/', 'index',  #only for testing
		'/submit', 'submit',
		)

class index:
	def GET(self):
		return open('index.html').read()

class submit:
	"""room = Room(('四平校区','西南八楼','322'),email='classone2010@gmail.com')"""
	def POST(self):
		room = self.check(web.input())
		room.save()
		print(room)
		web.SeeOther('/success')
	def check(self,inputs):
		#pdb.set_trace()
		try:
			arg1 = inputs['district'][:33]
			arg2 = inputs['building'][:33]
			arg3 = inputs['room'][:33]
			email= inputs['email'][:120]
			threshold = int(inputs['threshold'])
		except Exception, e:
			raise e
		return Room(format=(arg1,arg2,arg3), threshold=threshold, email=email)

app = web.application(urls, globals())
if __name__ == "__main__":
    app.run()
else:
    application = app.wsgifunc()