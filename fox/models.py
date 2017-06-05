from django.db import models


# from datetime import datetime

# Create your models here.

class Host(models.Model):
    '''
    主机名、ip、系统版本、内存、硬盘、制造商、cpu、厂商、生产商,SN
    '''
    hostname = models.CharField(max_length=50)
    ip = models.GenericIPAddressField()
    # os = models.CharField(max_length=50)
    # mem_free = models.CharField(max_length=50)
    # mem_usage = models.CharField(max_length=50)
    mem_total = models.CharField(max_length=50)
    # load_avg = models.CharField(max_length=50)
    disk = models.CharField(max_length=50)
    # vendor_id = models.CharField(max_length=50)
    # model_name = models.CharField(max_length=50)
    # cpu = models.CharField(max_length=50)
    # product = models.CharField(max_length=50)
    # Manufacturer = models.CharField(max_length=50)
    time = models.DateTimeField(max_length=50)
    # class Meta:
    #     verbose_name = '主机名'


class Task(models.Model):
    name = models.CharField(max_length=32, default='Cron')
    task = models.CharField(max_length=32)
class HostTask(models.Model):
    host = models.ForeignKey(Host,related_name='host_task')
    task = models.ForeignKey(Task,default='1')
    status = models.FloatField(Task,default='1')