from django.contrib import admin
from fox import models


class HostAdmin(admin.ModelAdmin):
    list_display = [
        'hostname',
        'ip',
        # 'os',
        'mem_total',
        # 'disk',
        # 'vendor_id',
        # 'model_name',
        # 'cpu',
        # 'product',
        # 'Manufacturer',
        'time'
    ]
class TaskAdmin(admin.ModelAdmin):
    list_display = [
        'name','task',
    ]

admin.site.register(models.Host, HostAdmin)
admin.site.register(models.Task,TaskAdmin)
admin.site.register(models.HostTask)
