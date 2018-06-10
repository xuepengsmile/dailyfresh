# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from models import *


class GoodsInfoAdmin(admin.ModelAdmin):
    list_per_page = 15
    list_display = ['id', 'gname', 'gprice', 'gunit', 'ginventory', 'gcontent', 'gtype']


class TypeInfoAdmin(admin.ModelAdmin):
    list_display = ['id', 'ttitle']


admin.site.register(GoodsInfo, GoodsInfoAdmin)
admin.site.register(TypeInfo, TypeInfoAdmin)
