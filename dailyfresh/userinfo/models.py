# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class UserInfo(models.Model):
    uname = models.CharField(max_length=10)
    upwd = models.CharField(max_length=40)
    ushouji = models.CharField(max_length=15, default='')
    uyoubian = models.CharField(max_length=8, default='')
    uemail = models.CharField(max_length=40)
    uaddress = models.CharField(max_length=40)
    class meta():
        db_table = 'userinfo'
