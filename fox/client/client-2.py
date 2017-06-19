#!/bin/env/python
# -*- coding: utf-8 -*-
import os, time, json
import urllib,urllib2


# 判断备份文件是否存在
def file_status():
    # 格式化日期
    date = time.strftime('%Y_%m_%d', time.localtime())
    backup_file_name = '/data/backup/rds_bak/syt_rds_' + date + '_00.tar.gz'
    # 格式化文件名
    print(backup_file_name)
    backup_file_status = os.path.exists(backup_file_name)
    # 判断该文件是否存在
    if backup_file_status is True:
        print('OK !')
        return 1
    else:
        print('Not OK !')
        return 0

class CPU():
    @staticmethod
    def version():
        cpu_version = os.popen("dmidecode -t 4|grep Version |awk -F ':'  '{print $2}' |awk 'NR==1'").read()
        if cpu_version == '' :
            return None
        return cpu_version

    @staticmethod
    def physical():
        cpu_physical = os.popen('cat /proc/cpuinfo| grep "physical id"| sort| uniq| wc -l').read()
        if cpu_physical == '' :
            return None
        return cpu_physical

    @staticmethod
    def cores():
        cpu_cores = os.popen("cat /proc/cpuinfo| grep 'cpu cores'| uniq|awk '{print $4}'").read()
        if cpu_cores  == '' :
            return None
        return cpu_cores

    @staticmethod
    def processor():
        cpu_processor = os.popen('cat /proc/cpuinfo| grep "processor"| wc -l').read()
        if cpu_processor == '' :
            return None
        return cpu_processor

def serial_number():
    sn = os.popen("dmidecode -t 1 |awk 'NR==9'|awk '{print $3}'").read()
    uuid = os.popen("dmidecode -t 1 |awk 'NR==10'|awk '{print $2}'").read()
    if len(sn) <= 4:
        return uuid
    else:
        return sn
def product():
    pro = os.popen("dmidecode -t 1 |awk 'NR==7'|awk '{print $3,$4}'").read()
    return pro
def http_post():
    date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    hostname = os.popen('hostname').read()
    ip = os.popen("ifconfig |grep 'inet addr:'|awk -F ':' 'NR==1{print $2}'|awk '{print $1}'").read()
    mem = os.popen("cat /proc/meminfo |awk 'NR==1{print $2}'").read()
    mem_total = round(int(mem) /(1024 * 1024))
    disk = os.statvfs("/")
    hd = {}
    hd['available'] = round(disk.f_bsize * disk.f_bavail / (1024 * 1024 * 1024))
    hd['capacity'] = round(disk.f_bsize * disk.f_blocks / (1024 * 1024 * 1024))
    hd['used'] = round(disk.f_bsize * disk.f_bfree / (1024 * 1024 * 1024))
    s = file_status()
    sn = serial_number()
    print(sn)
    data = {
        'hostname': hostname,
        'ip': ip,
        # 'status':10,
        'mem_total': mem_total,
        'time': date,
        'disk': hd['available'],
        'product':product(),
        'sn': sn,
        'cpu_version':CPU.version()
    }
    url = 'http://192.168.1.110:8000/fox/update_host/'
    data = urllib.urlencode(data).encode('utf-8')
    req = urllib2.Request(url, data=data)
    res = urllib2.urlopen(req)
    print(res)

    return 'ok'


if __name__ == '__main__':
    http_post()