from django.shortcuts import render
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from fox import models
import json
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count
# from Earth.forms import ArticleFrom, handle_uploaded_file, CategoryFrom, AboutFrom
from django.http import Http404


# Create your views here.

def update_status(pk):
    '''
    更新Task表记录
    统计每种task的状态,取平均值
    :return:
    '''
    t_count = models.HostTask.objects.filter(task_id=pk).count()
    t_status = models.HostTask.objects.filter(task_id=pk)
    t_list = []
    sum = 0
    for i in t_status:
        sum = sum + i.status
    try:
        t_avg = sum / t_count
    except:
        t_avg = 0
    t = models.Task.objects.filter(id=pk).update(status=t_avg)

    # print(t_avg)
    return True


def add(request):
    if request.method == 'POST':
        print('这里是POST的数据:', request.POST)
        type = request.POST.get('type')
        print(type)
        if type == 'task':
            new_name = request.POST.get('name')
            new_task = request.POST.get('task')
            new_status = request.POST.get('status')
            t = models.Task.objects.create(name=new_name, task=new_task, status=new_status)
        else:
            print('这是host')
    else:
        print('ok')
    return render(request, 'status.html')


def update(request):
    if request.method == 'POST':
        type = request.POST.get('type')
        print(type)
        if type == 'task':
            id = request.POST.get('id')
            new_name = request.POST.get('name')
            new_task = request.POST.get('task')
            t = models.Task.objects.filter(id=id).update(name=new_name, task=new_task)
        else:
            print('这是host')

    else:
        print('ok')
    return render(request, 'status.html')


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
        host_obj = models.Host.objects.all().values()
        # 取出cron所有记录

        task_obj = models.Task.objects.all().values()
        posts = pages(request, task_obj)
        task_count = models.Task.objects.all().count()
        # print(task_count)
        i = 1
        while i < task_count:
            # print(i)
            update_status(i)
            i += i
        return render(request, 'status.html', {'task': task_obj, 'host': host_obj, 'posts': posts})

# def getdata():
#     stat_obj = models.Host
#     return "%s(%s);" % ('callback', json.dumps(stat_obj))
