import os
hostname = os.popen('hostname').read()
ip = os.popen("ifconfig |grep 'inet addr:'|awk -F ':' 'NR==1{print $2}'|awk '{print $1}'").read()