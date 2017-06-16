from django.shortcuts import render
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from fox import models
import json,datetime
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count
# from Earth.forms import ArticleFrom, handle_uploaded_file, CategoryFrom, AboutFrom
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse

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
        print('posts', posts)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        posts = paginator.page(1)
        print('posts-new', posts)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        posts = paginator.page(paginator.num_pages)
        print('posts-e', posts)
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
        print(type)
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
    return render(request, 'task_table.html',{'posts': posts})
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
    return render(request, 'task_table.html',{'posts': posts})

def host_add(request):
    if request.method == 'POST':
        print('这里是更新的数据', request.POST)
        new_hostname = request.POST.get('hostname')
        new_ip = request.POST.get('ip')
        # new_status = request.POST.get('status')
        new_disk = request.POST.get('disk')
        new_mem = request.POST.get('mem_total')
        new_time = request.POST.get('time')
        t = models.Host.objects.create(hostname=new_hostname,ip=new_ip,disk=new_disk,time=new_time,mem_total=new_mem)
    else:
        print('ok')
    return render(request, 'status.html')


def update_host(request):
    if request.method == 'POST':
        print('这里是更新的数据', request.POST)
        new_hostname = request.POST.get('hostname')
        new_ip = request.POST.get('ip')
        # new_status = request.POST.get('status')
        new_disk = request.POST.get('disk')
        new_mem = request.POST.get('mem_total')
        new_time = request.POST.get('time')

        try:
            models.Host.objects.get(hostname=new_hostname)
        except ObjectDoesNotExist:
            print('创建')
            t = models.Host.objects.create(hostname=new_hostname,ip=new_ip,disk=new_disk,time=new_time,mem_total=new_mem)
        else:
            print('更新')
            t = models.Host.objects.filter(hostname=new_hostname).update(ip=new_ip,disk=new_disk,time=new_time,mem_total=new_mem)


    else:
        print('ok')
    host_obj = models.Host.objects.all().values()
    posts = pages(request, host_obj)
    return render(request, 'host_table.html',{'posts': posts})


def assets(request):
    host_obj = models.Host.objects.all().values()
    posts = pages(request, host_obj)
    if request.method == 'POST':
        if request.POST.get('type') == 'detail':
            hostneme = request.POST.get('hostname')
            print(hostneme)
            t = models.Host.objects.filter(hostname=hostneme)
            print(type(list(t.values())))
            for i in list(t.values()):
                t = (JsonResponse(i))

            return HttpResponse(t)
        else:
            return render(request, 'host.html',{'posts': posts,'host':host_obj})
    else:
        return render(request, 'host.html',{'posts': posts,'host':host_obj})
def tasks(request):
    task_obj = models.Task.objects.all().values()
    posts = pages(request, task_obj)
    return render(request, 'task.html', {'task': task_obj, 'posts': posts})
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
        print(t_host)
        t = models.HostTask.objects.filter(host_id=t_host).update(status=status)

        return render(request, 'status.html')
    else:
        #
        # print(task_count)
        i = 1
        # while i < task_count:
        #     # print(i)
        #     # update_status(i)
        #     i += i
        task_obj = models.Task.objects.all().values()
        host_obj = models.Host.objects.all().values()
        posts = pages(request, task_obj)
        return render(request, 'status.html', {'task': task_obj, 'host': host_obj, 'posts': posts})

# def getdata():
#     stat_obj = models.Host
#     return "%s(%s);" % ('callback', json.dumps(stat_obj))
