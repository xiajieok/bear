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

    t_avg = sum / t_count
    t = models.Task.objects.filter(id=pk).update(status=t_avg)

    # print(t_avg)
    return True


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
        # 取出cron所有记录

        task_obj = models.Task.objects.all().values()
        task_count = models.Task.objects.all().count()
        # print(task_count)
        i = 1
        while i < task_count:
            # print(i)
            update_status(i)
            i += i
        return render(request, 'status.html', {'task': task_obj})


def getdata():
    stat_obj = models.Host
    return "%s(%s);" % ('callback', json.dumps(stat_obj))
