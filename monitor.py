#!/usr/bin/env python
# coding=utf-8
#    Tongji University electricity charge low pre warning
#    C19<classone2010@gmail.com>

import urllib2  
import cookielib
import cStringIO
import gzip
from lxml import etree

class Monitor:
    def __init__(self):
	    self.cj = cookielib.CookieJar()
	    self.cj.clear()
	    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cj))  
	    opener.addheaders = [('User-agent','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.56 Safari/536.5'),\
	                         ('Connection','keep-alive'),\
	                         ('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'),\
	                         ('Accept-Charset','GBK,utf-8;q=0.7,*;q=0.3'),\
	                         ('Accept-Encoding','gzip'),\
	                         ('Accept-Language','zh-CN,zh;q=0.8'),\
	                         ('Cache-Control','max-age=0'),\
	                         ('Connection','keep-alive')]
	    urllib2.install_opener(opener)

    def get(self,url,data=None):
        resp = urllib2.urlopen(url,data)
        if resp.info().getheader('Content-Encoding') == 'gzip':
            zbuf=cStringIO.StringIO(resp.read())
            html = gzip.GzipFile(fileobj=zbuf,mode='rb').read()
        else:
            html = resp.read()
        return html

mon = Monitor()

def check_fee(rooms):
	url = 'http://nyglzx.tongji.edu.cn/web/datastat.aspx' 
	raw = """__EVENTTARGET=&__EVENTARGUMENT=&__LASTFOCUS=&__VIEWSTATE=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&__EVENTVALIDATION=/wEWMAK3pffoCgKehO/XDgKS2sqQDQKbhO/XDgLvo6/WAQKchO/XDgKco5mFBAKo7ZuOCQKQtOGrAwLGtc2eAwKUkP3jDgKphpG2AgL3ot33AgL3ov2mCAKR/qiJBgLpo8D8CQLqit2DCAKmxb3NAwKagoO1DwL7l4KfDgLI+KbeDgLOpvM+ApOWxbkCAtfasrgPAp7mkOoLAvuXgsEPArS90Z0GAsaKq7AOAsj4poAOAqiThtMDAtqFzUwC3YXNTAKok9bEAQLX2rL6DAKq0IqHBwK1odOhBAKo0PbrBgLKs5euBgLqyrSJDQL+gaXtDgLqyriJDQL+gantDgLeuZHECgK8w4S2BAKjm5WMBgLe09aaBAKn667gAwL85db2Aw48FruJ5jVZy/s5BGofTJ3W0f6d&\
			DistrictDown={0}&BuildingDown={1}&RoomnameText={2}&Submit=查询"""
	if isinsta(rooms,list):
		for room in rooms:
			check_fee(room)
	else:
		#sorry for the ugly code, the page is incredibly awful and strange,
		#it has to post a long nonsence __VIEWSTATE and html was full of 
		#tables, somehow lxml.etree coudn't parse correctly.
		html = mon.get(url,raw.format(*rooms.format))
		n 	 = html.find('剩余电量（kWh）</th>')
		table= html[n:n+400]
		cells= re.findall(re.compile('<td>(.*?)</td>'),table)
		fee = cells[3]
		fee = float(fee)
		if fee < rooms.threshold:
			sendmail(rooms.email, '快没电费啦！！！', '=w=')

