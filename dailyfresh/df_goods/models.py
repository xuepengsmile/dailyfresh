# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class TypeInfo(models.Model):
    ttitle = models.CharField(max_length=10)
    isDelete = models.BooleanField(default=False)

    def __str__(self):
        return self.ttitle.encode('utf-8')


class GoodsInfo(models.Model):
    gname = models.CharField(max_length=20)
    gpic = models.ImageField(upload_to='df_goods')
    gprice = models.DecimalField(max_digits=6, decimal_places=2)
    gunit = models.CharField(max_length=20, default='500g')
    isDelete = models.BooleanField(default=False)
    gclick = models.IntegerField()
    gintroduction = models.CharField(max_length=200)
    ginventory = models.IntegerField()
    gcontent = models.CharField(max_length=100)
    gtype = models.ForeignKey(TypeInfo)
