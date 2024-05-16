from django.contrib import admin
import os
from django.utils.safestring import mark_safe
from .models import *

project_name = os.path.split(os.getcwd())[1]
admin.site.site_header = project_name + "-管理员后台"
admin.site.site_title = project_name + "-超级管理员后台"
admin.site.index_title = project_name + "-超级管理员后台"
from django.contrib import admin

from django.utils.safestring import mark_safe
from .models import *




class ObjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'classes', 'latin_name', 'head', 'family', 'gender', 'feeding_habits', 'detail']
    search_fields = ['name']
admin.site.register(Object, ObjectAdmin)
class OcrAdmin(admin.ModelAdmin):
    list_display = ['username', 'add_time', 'result', 'ocr_time']
    search_fields = ['username', 'add_time', 'result', ]


admin.site.register(OcrLog, OcrAdmin)
