# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from models import *
from hashlib import sha1
import user_decorator
from df_goods.models import GoodsInfo


def register(request):
    context = {'title': '注册'}
    return render(request, 'userinfo/register.html', context)


def register_exit(request):
    username = request.GET.get('username')
    count = UserInfo.objects.filter(uname=username).count()
    return JsonResponse({'count': count})


def register_handle(request):
    # 密码用hash保存
    post = request.POST
    uname = post.get('user_name')
    pwd = post.get('pwd')
    cpwd = post.get('cpwd')
    email = post.get('email')

    if pwd != cpwd:
        return redirect('/user/register/')

    count = UserInfo.objects.filter(uname=uname).count()
    if count >= 1:
        return redirect('/user/register/')

    s1 = sha1()
    s1.update(pwd)
    pwd_sha = s1.hexdigest()

    user = UserInfo()
    user.uname = uname
    user.upwd = pwd_sha
    user.uemail = email
    user.save()

    return redirect('/user/login/')


def login(request):
    uname = request.COOKIES.get('uname', '')
    context = {'title': '用户登录', 'error_name': 0, 'error_pwd': 0, 'uname': uname}
    return render(request, 'userinfo/login.html', context)


def login_handle(request):
    # 判断用户名密码  重定向网址
    post = request.POST
    uname = post.get('username')
    pwd = post.get('pwd')
    jizhu = post.get('jizhu', 0)
    users = UserInfo.objects.filter(uname=uname)

    # 判断用户名
    count = UserInfo.objects.filter(uname=uname).count()
    if count == 0:
        context = {'title': '用户登录', 'error_name': 1, 'error_pwd': 0, 'uname': uname}
        return render(request, 'userinfo/login.html', context)

    # 判断密码
    user = UserInfo.objects.get(uname=uname)
    s1 = sha1()
    s1.update(pwd)
    pwd_sha = s1.hexdigest()

    if pwd_sha != user.upwd:
        context = {'title': '用户登录', 'error_name': 0, 'error_pwd': 1, 'uname': uname}
        return render(request, 'userinfo/login.html', context)
    else:
        # 登录后的网址
        url = request.COOKIES.get('url', '')
        if len(url) == 0:
            red = HttpResponseRedirect('/')
        else:
            red = HttpResponseRedirect(url)

        # 记住用户名
        if jizhu != 0:
            red.set_cookie('uname', uname)
        else:
            red.set_cookie('uname', '', max_age=-1)

        request.session['uname'] = uname
        request.session['user_id'] = users[0].id
        return red


@user_decorator.login
def info(request):
    goods_ids = request.COOKIES.get('goods_ids', '')
    goods_id_list = goods_ids.split(',')
    goods_list = []
    if len(goods_id_list):
        for goods_id in goods_id_list:
            goods = GoodsInfo.objects.get(id=int(goods_id))
            goods_list.append(goods)

    context = {'title': '用户中心', 'shopping_cart': 0, 'goods_list': goods_list}
    return render(request, 'userinfo/user_center_info.html', context)


@user_decorator.login
def site(request):
    context = {'title': '收货地址', 'shopping_cart': 0}
    return render(request, 'userinfo/user_center_site.html', context)


@user_decorator.login
def order(request):
    context = {'title': '订单信息', 'shopping_cart': 0}
    return render(request, 'userinfo/user_center_order.html', context)


def logout(request):
    request.session.flush()
    return HttpResponseRedirect('/')
