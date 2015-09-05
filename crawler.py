# -*- coding: utf-8 -*-

import os
import json
import sys
import re
import urllib2
import urllib
import requests
import cookielib
from datetime import datetime
from test_bs4 import *

reload(sys)  
sys.setdefaultencoding('utf-8')  

class Query(object):
    def __init__(self):
#        self.name = ''
#        self.pwd = ''
#        self.domain = ''
        self.cookieInstall()
        self.opener.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.57 Safari/537.36')]
    
    def cookieInstall(self):
        self.cj = cookielib.LWPCookieJar()
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cj))
        urllib2.install_opener(self.opener)

    def query(self, car_number):
        req = 'http://k.autohome.com.cn/%s/' %car_number
        res = urllib2.urlopen(req)
        return  res.read().replace('\r','')

    def query_add_comments(self, add_comments_url):
        res = urllib2.urlopen(add_comments_url)
        return  res.read().replace('\r','')

if __name__ == '__main__':
    car_number = sys.argv[1]
    myQuery = Query()
    html_doc = myQuery.query(car_number)
    word_of_mouth = get_beautiful_soup(html_doc)
    for sample in word_of_mouth:
        data = extract_mark(sample)
        comment = extract_comment(sample)
        data['comment'] = comment
        add_comments_url = get_add_comments_url(sample) 
        add_comments_html_doc = myQuery.query_add_comments(add_comments_url)
        print json.dumps(data, ensure_ascii = False) 
#    new_cookie = ''
#    for app_name in app:
#        data[app_name] = {}
#        oem_map = myQuery.load_channels(app_name)
#        for oem_code in oem_map:
#            new_cookie, activate_data = myQuery.query(app_name, start_date, end_date, oem_code, 'daily')
#            data[app_name][oem_code] = activate_data
#    fobj = open(os.path.join(cur_path, 'cookie'), 'w')
#    fobj.write('cookie = "' + new_cookie + '"')
#    print json.dumps(data)
