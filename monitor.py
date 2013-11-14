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
url = 'http://nyglzx.tongji.edu.cn/web/datastat.aspx' 
raw = """__EVENTTARGET=&__EVENTARGUMENT=&__LASTFOCUS=&__VIEWSTATE=%2FwEPDwUKLTYwNjgwNDAyOQ8WDB4Jcm9vbXRhYmxlBQ9zcGRhdGFfcm9vbXZpZXceCWRhdGF0YWJsZQULc3BkYXRhX3ZpZXceBmFkZHN0cmUeB2J1aWxkaWQFBDQ0MjUeCnJvb21uYW1laWQFBDQ1NjUeBGZsYWcFATEWAgIDD2QWCgIDDxBkZBYBAgJkAgUPEA8WBB4NRGF0YVRleHRGaWVsZAUIUk9PTU5BTUUeC18hRGF0YUJvdW5kZ2QQFRwR6LWk5bOw6Lev5ZCO5YukMgAQ5ZCO5Yuk5bel5a%2BTICAgIBLlkI7li6Tlhazlr5PkuInnm7gP6Kej5pS%2B5qW8ICAgICAgD%2BmdkuW5tOalvCAgICAgIBDopb%2FljJfkuozmpbwgICAgEOilv%2BWMl%2BS4iealvCAgICAQ6KW%2F5YyX5Zub5qW8ICAgIBDopb%2FljJfkupTmpbwgICAgEOilv%2BWMl%2BS4gOalvCAgICAQ6KW%2F5Y2X5YWr5qW8ICAgIBDopb%2FljZfkuozmpbwgICAgEOilv%2BWNl%2BS5nealvCAgICAQ6KW%2F5Y2X5LiD5qW8ICAgIBDopb%2FljZfkuInmpbwgICAgEeilv%2BWNl%2BWNgeS6jOalvCAgEOilv%2BWNl%2BWNgealvEHmpbwQ6KW%2F5Y2X5Y2B5qW8QualvBHopb%2FljZfljYHkuIDmpbwgIBDopb%2FljZfkuIDmpbwgICAgD%2BWtpuS4iealvCAgICAgIA%2Flrablm5vmpbwgICAgICAP5a2m5LqU5qW8ICAgICAgEeeglOeptueUn%2BWFrOWvkzMgEeeglOeptueUn%2BWFrOWvkzQAEOeglOeptueUn%2BWFrOWvkzQR56CU56m255Sf5YWs5a%2BTNQAQ56CU56m255Sf5YWs5a%2BTNRUcEei1pOWzsOi3r%2BWQjuWLpDIAEOWQjuWLpOW3peWvkyAgICAS5ZCO5Yuk5YWs5a%2BT5LiJ55u4D%2Bino%2BaUvualvCAgICAgIA%2FpnZLlubTmpbwgICAgICAQ6KW%2F5YyX5LqM5qW8ICAgIBDopb%2FljJfkuInmpbwgICAgEOilv%2BWMl%2BWbm%2BalvCAgICAQ6KW%2F5YyX5LqU5qW8ICAgIBDopb%2FljJfkuIDmpbwgICAgEOilv%2BWNl%2BWFq%2BalvCAgICAQ6KW%2F5Y2X5LqM5qW8ICAgIBDopb%2FljZfkuZ3mpbwgICAgEOilv%2BWNl%2BS4g%2BalvCAgICAQ6KW%2F5Y2X5LiJ5qW8ICAgIBHopb%2FljZfljYHkuozmpbwgIBDopb%2FljZfljYHmpbxB5qW8EOilv%2BWNl%2BWNgealvELmpbwR6KW%2F5Y2X5Y2B5LiA5qW8ICAQ6KW%2F5Y2X5LiA5qW8ICAgIA%2FlrabkuInmpbwgICAgICAP5a2m5Zub5qW8ICAgICAgD%2BWtpuS6lOalvCAgICAgIBHnoJTnqbbnlJ%2Flhazlr5MzIBHnoJTnqbbnlJ%2Flhazlr5M0ABDnoJTnqbbnlJ%2Flhazlr5M0EeeglOeptueUn%2BWFrOWvkzUAEOeglOeptueUn%2BWFrOWvkzUUKwMcZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2RkAhEPDxYCHgRUZXh0BR%2Flm5vlubPmoKHljLropb%2FljZflhavmpbwgICAgMzIyZGQCEw8PFgQfCAUz6LCD6K%2BV6Zi25q6177ya5aaC5pyJ5LiN5L6%2F5LmL5aSE77yM5pWs6K%2B35Y6f6LCF77yBHgdWaXNpYmxlaGRkAhUPPCsADQEADxYEHwdnHgtfIUl0ZW1Db3VudAIaZBYCZg9kFhgCAQ9kFghmDw8WAh8IBQoyMDEzLTExLTE0ZGQCAQ8PFgIfCAUINCw2OTYuMDBkZAICDw8WAh8IBQg0LDg5Ny4yNWRkAgMPDxYCHwgFBjIwMS4yNWRkAgIPZBYIZg8PFgIfCAUKMjAxMy0xMS0xM2RkAgEPDxYCHwgFCDQsNjg1Ljc1ZGQCAg8PFgIfCAUINCw4OTcuMjVkZAIDDw8WAh8IBQYyMTEuNTBkZAIDD2QWCGYPDxYCHwgFCjIwMTMtMTEtMTJkZAIBDw8WAh8IBQg0LDY4NC4xMGRkAgIPDxYCHwgFCDQsODk3LjI1ZGQCAw8PFgIfCAUGMjEzLjE1ZGQCBA9kFghmDw8WAh8IBQoyMDEzLTExLTExZGQCAQ8PFgIfCAUINCw2ODIuNDBkZAICDw8WAh8IBQg0LDg5Ny4yNWRkAgMPDxYCHwgFBjIxNC44NWRkAgUPZBYIZg8PFgIfCAUKMjAxMy0xMS0xMGRkAgEPDxYCHwgFCDQsNjY3Ljg1ZGQCAg8PFgIfCAUINCw4OTcuMjVkZAIDDw8WAh8IBQYyMjkuNDBkZAIGD2QWCGYPDxYCHwgFCjIwMTMtMTEtMDlkZAIBDw8WAh8IBQg0LDY2NS4zMGRkAgIPDxYCHwgFCDQsODk3LjI1ZGQCAw8PFgIfCAUGMjMxLjk1ZGQCBw9kFghmDw8WAh8IBQoyMDEzLTExLTA4ZGQCAQ8PFgIfCAUINCw2NjIuODBkZAICDw8WAh8IBQg0LDg5Ny4yNWRkAgMPDxYCHwgFBjIzNC40NWRkAggPZBYIZg8PFgIfCAUKMjAxMy0xMS0wN2RkAgEPDxYCHwgFCDQsNjYwLjcwZGQCAg8PFgIfCAUINCw4OTcuMjVkZAIDDw8WAh8IBQYyMzYuNTVkZAIJD2QWCGYPDxYCHwgFCjIwMTMtMTEtMDZkZAIBDw8WAh8IBQg0LDY1OS4wMGRkAgIPDxYCHwgFCDQsODk3LjI1ZGQCAw8PFgIfCAUGMjM4LjI1ZGQCCg9kFghmDw8WAh8IBQoyMDEzLTExLTA1ZGQCAQ8PFgIfCAUINCw2NTcuNDBkZAICDw8WAh8IBQg0LDg5Ny4yNWRkAgMPDxYCHwgFBjIzOS44NWRkAgsPDxYCHwloZGQCDA9kFgJmD2QWBgIBDw8WAh8IBREg56ysMemhtS8g5YWxM%2BmhtWRkAgMPDxYCHgdFbmFibGVkaGRkAgUPDxYCHwtoZGQYAQUJR3JpZFZpZXcxDzwrAAoBCAIDZCHsRjRP6T2oAo96lHqMZrhth%2FPR&__EVENTVALIDATION=%2FwEWMAK3pffoCgKehO%2FXDgKS2sqQDQKbhO%2FXDgLvo6%2FWAQKchO%2FXDgKco5mFBAKo7ZuOCQKQtOGrAwLGtc2eAwKUkP3jDgKphpG2AgL3ot33AgL3ov2mCAKR%2FqiJBgLpo8D8CQLqit2DCAKmxb3NAwKagoO1DwL7l4KfDgLI%2BKbeDgLOpvM%2BApOWxbkCAtfasrgPAp7mkOoLAvuXgsEPArS90Z0GAsaKq7AOAsj4poAOAqiThtMDAtqFzUwC3YXNTAKok9bEAQLX2rL6DAKq0IqHBwK1odOhBAKo0PbrBgLKs5euBgLqyrSJDQL%2BgaXtDgLqyriJDQL%2BgantDgLeuZHECgK8w4S2BAKjm5WMBgLe09aaBAKn667gAwL85db2Aw48FruJ5jVZy%2Fs5BGofTJ3W0f6d&DistrictDown=%E5%9B%9B%E5%B9%B3%E6%A0%A1%E5%8C%BA&BuildingDown=%E8%A5%BF%E5%8D%97%E5%85%AB%E6%A5%BC++++&RoomnameText={0}&Submit=%E6%9F%A5%E8%AF%A2"""

#sorry for the ugly code, the page is incredibly awful and strange,
#it has to post a long nonsence __VIEWSTATE and html was full of 
#tables, somehow lxml.etree coudn't parse correctly.
html = mon.get(url,raw.format('322'))
n 	 = html.find('剩余电量（kWh）</th>')
table= html[n:n+400]
cells= re.findall(re.compile('<td>(.*?)</td>'),table)
fee = cells[3]
fee = float(fee)

if fee < 10:
	sendmail('classone2010@gmail.com','快没电费啦！！！','=w=')
