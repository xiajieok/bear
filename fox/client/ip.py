import re, json

d = ['/dev/mapper/VolGroup-lv_root   36G   15G   19G  45% /',
     '/dev/vda1                     485M   32M  428M   7% /boot']
pattern = re.compile(r'M')
list_d = []
def disk():
    for i in d:
        i = i.split()
        list_v = []
        for v in i:
            # print(v)
            if 'M' in v:
                v = v/1024
                print(v)
            list_v.append(v)
        key = ['dir', 'all', 'used', 'space', 'used%', 'mount']
        tmp = dict(zip(key, list_v))
        s = list_d.append(tmp)
    print(tmp)
    # new = json.dumps(list_d)
    # return s
disk()

