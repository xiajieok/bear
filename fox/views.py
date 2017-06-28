from django.shortcuts import render
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from fox import models
import json, datetime
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count
# from Earth.forms import ArticleFrom, handle_uploaded_file, CategoryFrom, AboutFrom
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from fox.SaltApi import SaltAPI
host_obj = models.Host.objects.all().values()


# 取出cron所有记录


# Create your views here.
def pages(request, q_all):
    '''
    分页功能实现,根据SQL查询内容,设定分多少页,输出
    :param request:
    :param blog_all:
    :return:
    '''
    paginator = Paginator(q_all, 4)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        posts = paginator.page(paginator.num_pages)
    return posts


# def add(request):
#     if request.method == 'POST':
#         print('这里是POST的数据:', request.POST)
#         type = request.POST.get('type')
#         print(type)
#         if type == 'task':
#             new_name = request.POST.get('name')
#             new_task = request.POST.get('task')
#             new_status = request.POST.get('status')
#             print(new_name, new_task, new_status)
#             t = models.Task.objects.create(name=new_name, task=new_task, status=new_status)
#         else:
#             print('这是host')
#     else:
#         print('ok')
#     return render(request, 'status.html')



def delete(request):
    if request.method == 'POST':
        print('这里是POST的数据:', request.POST)
        type = request.POST.get('type')
        if type == 'task':
            new_name = request.POST.get('name')
            # print(new_name,new_task,new_status)
            t = models.Task.objects.get(name=new_name).delete()
        else:
            print('这是host')
    else:
        print('ok')
    task_obj = models.Task.objects.all().values()
    posts = pages(request, task_obj)
    return render(request, 'task_table.html', {'posts': posts})
    # return render(request, 'status.html')


def update(request):
    if request.method == 'POST':
        print('这里是更新的数据', request.POST)
        new_name = request.POST.get('name')
        new_task = request.POST.get('task')
        new_status = '100'
        print(new_name, new_task)

        try:
            models.Task.objects.get(name=new_name)
        except ObjectDoesNotExist:
            print('创建')
            t = models.Task.objects.create(name=new_name, task=new_task, status=new_status)
        else:
            print('更新')
            t = models.Task.objects.filter(name=new_name).update(task=new_task)



    else:
        print('ok')
    task_obj = models.Task.objects.all().values()
    posts = pages(request, task_obj)
    return render(request, 'task_table.html', {'posts': posts})


def host_add(request):
    if request.method == 'POST':
        print('这里是更新的数据', request.POST)
        new_hostname = request.POST.get('hostname')
        new_ip = request.POST.get('ip')
        # new_status = request.POST.get('status')
        new_disk = request.POST.get('disk')
        new_mem = request.POST.get('mem_total')
        new_time = request.POST.get('time')
        t = models.Host.objects.create(hostname=new_hostname, ip=new_ip, disk=new_disk, time=new_time,
                                       mem_total=new_mem)
    else:
        print('ok')
    return render(request, 'status.html')


def update_host(request):
    if request.method == 'POST':
        print('这里是更新的数据', request.POST)
        new_hostname = request.POST.get('hostname')
        new_ip = request.POST.get('ip')
        # new_status = request.POST.get('status')
        tmp_disk = request.POST.get('disk')
        t = json.loads(tmp_disk)

        new_mem = request.POST.get('mem_total')
        new_cpu_version = request.POST.get('cpu_version')
        new_time = request.POST.get('time')
        new_sn = request.POST.get('sn')
        new_product = request.POST.get('product')
        new_disk = 100
        host_sn = models.Host.objects.get(sn=new_sn).sn

        # 更新Disk
        all = 0
        used = 0
        for i in t:
            capacity = dict(i)['all']
            all = all + int(capacity)
            tmp_used = dict(i)['used']
            used = used + int(tmp_used)
            use = dict(i)['used%'][0:-1]
            new_partition = dict(i)['mount']
            new_available = dict(i)['space']
            updated_values = {"host_id": host_sn,
                              "used": used,
                              "use": use,
                              "capacity": capacity,
                              "available": new_available,
                              "partition": new_partition}
            print(updated_values)
            m = models.Disk.objects.update_or_create(defaults=updated_values, host_id=host_sn, partition=new_partition)

        # 更新主机表
        new_capacity = all
        new_used = used
        host_updated_values = {
            "ip": new_ip, "time": new_time, 'mem_total': new_mem, 'sn': new_sn, 'product': new_product,
            'cpu_version': new_cpu_version, 'disk': new_capacity}
        models.Host.objects.update_or_create(defaults=host_updated_values, sn=host_sn)


    else:
        print('ok')
    host_obj = models.Host.objects.all().values()
    posts = pages(request, host_obj)
    return render(request, 'host_table.html', {'posts': posts})


class Asset(object):
    host_obj = models.Host.objects.all().values()
    print(host_obj)

    def host(slef):
        print('self', slef.request)
        posts = pages(slef.request, host_obj)
        print('posts', posts)
        if slef.request.method == 'POST':
            print('展示主机详情')
            if slef.request.POST.get('type') == 'detail':
                hostname = slef.request.POST.get('hostname')
                sn = models.Host.objects.get(hostname=hostname).sn
                print(sn)
                used_obj = models.Disk.objects.filter(host_id=sn).values()
                print(used_obj)
                n = 0
                m = 0
                for i in list(used_obj.values()):
                    n = n + i['used']
                    m = m + i['capacity']
                used = n / m * 100
                obj_host = models.Host.objects.filter(hostname=hostname)
                for i in list(obj_host.values()):
                    print(i)
                    i['used'] = float('%.2f' % used)
                    ss = (JsonResponse(i))
                return HttpResponse('haha')
            else:
                print('展示主机信息')
                return render(slef.request, 'host.html', {'posts': posts, 'host': host_obj})
        else:
            print('GET:展示主机信息')
            print('GET:展示主机信息', posts)
            print('GET:展示主机信息', host_obj)
            return render(slef.request, 'host.html', {'posts': posts, 'host': host_obj})


def assets(request):
    # Asset.host(request)
    host_obj = models.Host.objects.all().values()
    posts = pages(request, host_obj)
    if request.method == 'POST':
        if request.POST.get('type') == 'detail':
            hostname = request.POST.get('hostname')
            sn = models.Host.objects.get(hostname=hostname).sn
            used_obj = models.Disk.objects.filter(host_id=sn).values()
            n = 0
            m = 0
            for i in list(used_obj.values()):
                n = n + i['used']
                m = m + i['capacity']
            used = n / m * 100
            obj_host = models.Host.objects.filter(hostname=hostname)
            for i in list(obj_host.values()):
                i['used'] = float('%.2f' % used)
                t = (JsonResponse(i))
            return HttpResponse(t)
        else:
            return render(request, 'host.html', {'posts': posts, 'host': host_obj})
    else:
        return render(request, 'host.html', {'posts': posts, 'host': host_obj})


def tasks(request):
    task_obj = models.Task.objects.all().values()
    posts = pages(request, task_obj)

    return render(request, 'task.html', {'task': task_obj, 'posts': posts})


def cc(request):
    t = models.Disk.objects.values('use').all()
    count = 0
    # print(type(t))
    for i in t:
        print(type(i))
        for j in i.values():
            print(j)
        count +=  j
    avg = count / len(t)
    l = []
    l.append(avg)
    l.append(count)
    return l

def index(request):
    if request.method == 'POST':
        print('这里是POST的数据:', request.POST)
        res = request.POST
        # 主机任务状态
        status = res['status']
        hostname = res['hostname']
        ip = res['ip']
        # print(hostname)
        # 写入数据库HostTask
        t_host = models.Host.objects.get(ip=ip).id
        t = models.HostTask.objects.filter(host_id=t_host).update(status=status)

        return render(request, 'status.html')
    else:
        avg = cc(request)
        print(avg)
        task_obj = models.Task.objects.all().values()
        host_obj = models.Host.objects.all().values()
        posts = pages(request, task_obj)
        return render(request, 'status.html', {'task': task_obj, 'host': host_obj, 'posts': posts,'avg':avg})

def cmd(request):
    if request.method == 'POST':
        print(request.method)
        salt = SaltAPI(url='https://192.168.1.30:8000', username='saltapi', password='salt')
        # params = {'client':'wheel', 'fun':'key.list_all', 'tgt':'*'}
        # params = {'client':'local', 'fun':'cmd.run', 'tgt':'*','arg':'free -m'}
        arg = request.POST.get('cmd')
        tgt = 'Dev-BJ-JRS-192.168.1.31'
        res = salt.cmd(tgt,arg)['return'][0]
        print(res)
        return  render(request,'cmd_res.html',{'cmd':res})
    else:
        print('Hello Get !!!')
        host_obj = ['Dev-BJ-JRS-192.168.1.31','Dev-BJ-XJ-192.168.1.40']

        return render(request,'cmd.html',{'host':host_obj})



# def getdata():
#     stat_obj = models.Host
#     return "%s(%s);" % ('callback', json.dumps(stat_obj))
