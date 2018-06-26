# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.http import JsonResponse
from models import *
from userinfo import user_decorator


@user_decorator.login
def cart(request):
    user_id = request.session['user_id']
    cartlist = CartInfo.objects.filter(user_id=user_id)
    cart_count = len(cartlist)
    context = {'title': '购物车', 'shopping_cart': 0,
               'cartlist': cartlist, 'cart_count': cart_count}
    return render(request, 'df_cart/cart.html', context)


@user_decorator.login
def addcart(request, goodid):
    user_id = request.session['user_id']
    carts = CartInfo.objects.filter(user_id=user_id, goods_id=goodid)
    if len(carts) >= 1:
        cart = carts[0]
        cart.count += 1
        cart.save()
    else:
        cart = CartInfo()
        cart.user_id = user_id
        cart.goods_id = goodid
        cart.count = 1
        cart.save()

    # 计算用户的购物车数量
    cart_temp = CartInfo.objects.filter(user_id=user_id)
    # 购物车数量加入cookie
    cart_count = request.session['count'] = len(cart_temp)
    data = {'cart_count': cart_count}
    if request.is_ajax():
        return JsonResponse(data)
    else:
        return redirect('/cart/')


@user_decorator.login
def edit(request, cartid, count):
    try:
        cart = CartInfo.objects.get(pk=int(cartid))
        count1 = cart.count =int(count)
        cart.save()
        data = {'ok': 0}
    except Exception as e:
        data = {'ok': count1}

    return JsonResponse(data)


@user_decorator.login
def delete(request, cartid):
    try:
        cart = CartInfo.objects.get(pk=int(cartid))
        cart.delete()
        cart_count = CartInfo.objects.filter(user=cart.user).count()
        data = {'cart_count': cart_count}
        # 购物车数量加入session
        request.session['count'] = cart_count
    except Exception as e:
        data = {'ok': 10}

    return JsonResponse(data)
