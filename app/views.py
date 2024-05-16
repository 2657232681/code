"""
Definition of views.
"""
import base64
from datetime import datetime
from django.shortcuts import render
from django.http import HttpRequest, JsonResponse, HttpResponseRedirect
from .forms import RegsiterForm
from django.contrib.auth.models import User
from django.views.generic import View
from django.contrib.auth import authenticate, login, logout
import uuid, math
import shutil, numpy as np
from django.shortcuts import render
import numpy as np
import os
from io import BytesIO
from numpy import linalg as LA
from .models import *
import glob, cv2
import PIL.Image as PImage
import json
from PIL import Image as PIL_Image
import random, requests


def checkLogin(func):
    def check(request, *args, **kwargs):
        if not request.user.is_anonymous:

            return func(request, *args, **kwargs)
        else:
            return HttpResponseRedirect("/login")

    return check


def calculate_neighboring_pages(current_page, total_pages):
    # 限制页码范围在1到总页数之间
    current_page = max(0, min(current_page, total_pages))

    # 计算开始和结束的页码
    start_page = max(0, current_page - 2)
    end_page = min(total_pages, current_page + 2)

    # 如果需要展示5个页码，则根据实际情况调整两端的页码
    while len(range(start_page, end_page + 1)) < 5:
        if start_page > 1:
            start_page -= 1
        elif end_page < total_pages:
            end_page += 1
        else:
            break

    # 获取并返回相邻的5页码列表
    neighboring_pages = list(range(start_page, end_page ))

    return neighboring_pages


def ocr_log(request):
    username = request.user.username
    page = request.GET.get('page', 0)
    page = int(page)

    logs = OcrLog.objects.filter(username=username).order_by("-id")
    count = logs.count()
    # 生成page附近的几个页码
    page_list = calculate_neighboring_pages(page, math.ceil(count / 15))

    page_list.sort()
    print(page_list, page)
    return render(request, 'ocr_log.html',
                  {"logs": logs[page * 15:(page + 1) * 15],
                   "page": page, "count": count,
                   "page_list": page_list,
                   "title": "识别日志", "page_count": page * 15,
                   "username": username}
                  )


@checkLogin
def changepwd(request):
    username = request.user.username
    if request.method == "GET":
        return render(request, "change_password.html", {
            "username": username
        })
    else:
        password = request.POST.get("password")
        new_password = request.POST.get("new_password")
        new_password2 = request.POST.get("new_password2")
        if new_password != new_password2:
            return JsonResponse({"code": 500, "msg": "新密码两次输入不一致!"})
        user = authenticate(username=username, password=password)
        if user:
            user.set_password(new_password)
            user.save()
            return JsonResponse({"code": 200, "msg": "修改成功!"})
        else:
            return JsonResponse({"code": 500, "msg": "密码错误!"})


def login_user(request):
    if request.method == "GET":
        return render(request, "login.html", {"title": "登录", })
    else:
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return JsonResponse({"code": 200, "msg": "登录成功!"})

        return JsonResponse({"code": 500, "msg": "用户名或密码错误!"})


@checkLogin
def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    if request.method == "GET":
        return render(
            request,
            'index.html',
            {
                'title': '首页',
                'year': datetime.now().year,
            }
        )


def register(request):
    """Renders the contact page."""
    if request.method == "GET":
        return render(
            request,
            'register.html',
            {
                'title': '用户注册',
                "form": RegsiterForm(),
            }
        )
    if request.method == "POST":
        form = RegsiterForm(request.POST)

        if form.is_valid():

            if form.cleaned_data["password"] != form.cleaned_data["password2"]:
                return JsonResponse({
                    "code": 500,
                    "msg": "两次密码不一致"
                })
            try:
                user = User.objects.get(username=form.cleaned_data["username"])
                return JsonResponse({"code": 500, "msg": "账号已存在!"})
            except:
                User.objects.create_user(username=form.cleaned_data["username"],
                                         password=form.cleaned_data["password2"])
                user = User.objects.get(username=form.cleaned_data["username"])
                login(request, user)
                return JsonResponse({"code": 200, "msg": "注册成功！"})
            return JsonResponse({"code": 200, "msg": "注册成功!请登录查看"})
        else:
            return JsonResponse({"code": 500, "msg": "请输入正确的信息"})
    return render(
        request,
        'register.html',
        {
            'title': '用户注册',
            "form": RegsiterForm(),

            'year': datetime.now().year,
        }
    )
