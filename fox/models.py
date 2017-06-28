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
    cpu_version = models.CharField(max_length=50,default='Xeon')
    product = models.CharField(max_length=50,default='Dell')
    # Manufacturer = models.CharField(max_length=50)
    sn = models.CharField(max_length=40,primary_key=True)
    time = models.DateTimeField(max_length=50)
    idc = models.ForeignKey('IDC',null=True, blank=True)

    # class Meta:
    #     verbose_name = '主机名'
class Disk(models.Model):
    host = models.ForeignKey(Host,related_name='host_disk')
    partition = models.CharField(max_length=50)
    used = models.IntegerField()
    use = models.IntegerField(default=0)
    capacity = models.IntegerField()
    available = models.IntegerField()
class Memory(models.Model):
    host = models.ForeignKey(Host,related_name='host_mem')
    capacity = models.IntegerField(u'内存大小（MB)')
class Task(models.Model):
    name = models.CharField(primary_key=True,max_length=32, default='Cron')
    task = models.CharField(max_length=32)
    status = models.FloatField(default='1')
class HostTask(models.Model):
    host = models.ForeignKey(Host,related_name='host_task')
    task = models.ForeignKey(Task,default='1')
    status = models.FloatField(Task,default='100')
class IDC(models.Model):
    name = models.CharField(max_length=20, verbose_name=u'机房名称',unique=True)
    type = models.CharField(max_length=20, verbose_name=u'机房类型',blank=True,null=True)
    location = models.CharField(max_length=30, verbose_name=u'机房位置',blank=True,null=True)
    memo = models.TextField(max_length=50, blank=True, verbose_name=u'备注',null=True)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = '机房'
        verbose_name_plural = "机房"