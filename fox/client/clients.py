#!/bin/env/python
# -*- coding: utf-8 -*-
import os,time,json
from urllib.request import Request
import urllib
from urllib import request, parse
from urllib.error import HTTPError

#判断备份文件是否存在
def file_status():
    date = time.strftime('%Y_%m_%d',time.localtime())
    #格式化日期

    backup_file_name = '/data/backup/rds_bak/syt_rds_' + date + '_00.tar.gz'
    #格式化文件名
    print(backup_file_name)
    backup_file_status  = os.path.exists(backup_file_name)
    #判断该文件是否存在
    if backup_file_status is True:
        print('OK !')
        return 1
    else:
        print('Not OK !')
        return 0
def http_post():
    hostname = os.popen('hostname').read()
    ip = os.popen("ifconfig |grep 'inet addr:'|awk -F ':' 'NR==1{print $2}'|awk '{print $1}'").read()
    s = file_status()
    data = {
        'hostname':hostname,
        'ip':'192.168.1.110',
        # 'status':10,
        'mem_total':8,
        'time':'2017-06-14 06:00',
        'disk':512
    }
    url = 'http://192.168.1.110:8000/fox/add/'
    data = parse.urlencode(data).encode('utf-8')
    req = request.Request(url,data=data)
    res = request.urlopen(req)
    print(res)

    return 'ok'
if __name__ == '__main__':
    http_post()