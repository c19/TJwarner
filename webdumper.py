#!/usr/bin/env python
# coding=utf-8
#    webdumper simplify
#    C19<classone2010@gmail.com>


import urllib2
import cookielib
import cStringIO
import gzip

class Webdumper(object):
    def __init__(self, cookie=None, proxy=None):
	    self.cj = cookielib.CookieJar()
	    self.cj.clear()
	    proxy  = urllib2.ProxyHandler(proxy)
	    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cj), proxy) 
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
        self.html = html
        return self.html