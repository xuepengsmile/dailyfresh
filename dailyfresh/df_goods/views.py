# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.shortcuts import render
from models import *
from django.core.paginator import Paginator
from df_cart.models import CartInfo


def index(request):
    typelist = TypeInfo.objects.all()
    type0 = typelist[0].goodsinfo_set.order_by('-id')[0:4]
    type00 = typelist[0].goodsinfo_set.order_by('-gclick')[0:4]
    type1 = typelist[1].goodsinfo_set.order_by('-id')[0:4]
    type11 = typelist[1].goodsinfo_set.order_by('-gclick')[0:4]
    type2 = typelist[2].goodsinfo_set.order_by('-id')[0:4]
    type22 = typelist[2].goodsinfo_set.order_by('-gclick')[0:4]
    type3 = typelist[3].goodsinfo_set.order_by('-id')[0:4]
    type33 = typelist[3].goodsinfo_set.order_by('-gclick')[0:4]
    type4 = typelist[4].goodsinfo_set.order_by('-id')[0:4]
    type44 = typelist[4].goodsinfo_set.order_by('-gclick')[0:4]
    type5 = typelist[5].goodsinfo_set.order_by('-id')[0:4]
    type55 = typelist[5].goodsinfo_set.order_by('-gclick')[0:4]

    count = request.session.get('count')
    context = {'title': '天天生鲜', 'shopping_cart': 1,
               'type0': type0, 'type00': type00,
               'type1': type1, 'type11': type11,
               'type2': type2, 'type22': type22,
               'type3': type3, 'type33': type33,
               'type4': type4, 'type44': type44,
               'type5': type5, 'type55': type55,
               'count': count}
    return render(request, 'df_goods/index.html', context)


def detail(request, gid):
    good = GoodsInfo.objects.get(id=int(gid))
    newgood_list = good.gtype.goodsinfo_set.order_by('-id')[0:2]
    good.gclick += 1
    good.save()

    count = request.session.get('count')
    context = {'shopping_cart': 1, 'title': '商品详情',
               'good': good, 'count': count,
               'newgood_list': newgood_list}
    response = render(request, 'df_goods/detail.html', context)

    # 最近浏览
    goods_ids = request.COOKIES.get('goods_ids', '')
    if goods_ids != '':
        goods_id_list = goods_ids.split(',')
        # 判断是否存在
        if goods_id_list.count(gid) >= 1:
            goods_id_list.remove(gid)
        # 添加到第一位
        goods_id_list.insert(0, gid)
        if len(goods_id_list) >= 6:
            del goods_id_list[5]
        goods_ids = ','.join(goods_id_list)
    else:
        goods_ids = gid

    response.set_cookie('goods_ids', goods_ids)

    return response


def list(request, typeid, pageid, orderid):
    typeinfo = TypeInfo.objects.get(id=int(typeid))
    newgood_list = typeinfo.goodsinfo_set.order_by('-id')[0:2]
    if orderid == '1':
        goods_list = typeinfo.goodsinfo_set.order_by('-id')
    if orderid == '2':
        goods_list = typeinfo.goodsinfo_set.order_by('-gprice')
    if orderid == '3':
        goods_list = typeinfo.goodsinfo_set.order_by('-gclick')
    if orderid == '4':
        goods_list = typeinfo.goodsinfo_set.order_by('gprice')

    page_object = Paginator(goods_list, 2)
    goodpage = page_object.page(int(pageid))

    count = request.session.get('count')

    context = {'shopping_cart': 1, 'title': '天天生鲜-商品列表',
               'newgood_list': newgood_list, 'goodpage': goodpage,
               'page_object': page_object, 'typeinfo': typeinfo,
               'orderid': orderid, 'count': count}
    return render(request, 'df_goods/list.html', context)
