#!/bin/env python3
import sys

mobile = sys.argv[1]
s = mobile.split(',')
tup1 = tuple(s)
#strip('()')去掉两头括号
s_tmp = '"' + str(tup1).strip('()') + '"'
print(s_tmp)