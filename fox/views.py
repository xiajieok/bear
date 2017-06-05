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
def index(request):
    if request.method == 'POST':
        print('这里是POST的数据:', request.POST)
    else:
        #显示计划任务名称,信息,状态
        task_name = models.Task.objects.values_list('name')
        task_info = models.Task.objects.values_list('task')

        status_obj = models.HostTask.objects.all().values()

        task_name_list = []
        task_info_list = []
        for i in list(task_name):
            for j in i:
                task_name_list.append(j)
        for i in list(task_info):
            for j in i:
                task_info_list.append(j)
        cron = dict(zip(task_name_list, task_info_list))
        print(cron)

        return render(request,'status.html',{'task':cron,'status':status_obj})
def getdata():
    stat_obj = models.Host
    return "%s(%s);" % ('callback', json.dumps(stat_obj))
