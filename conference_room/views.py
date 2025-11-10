import time

from django.http import HttpResponse, HttpResponseRedirect, StreamingHttpResponse
from django.shortcuts import render

from conference_room.models import UserManager, UserCompere
from tools.md5 import pass_md5


# Create your views here.

def conference_home(request):
    """
    # Auther: 李东阳
    会议室主页视图函数
    :param request:
    :return:
    """
    if request.method == 'GET':
        return render(request, 'conference_room/home.html')
    else:
        return HttpResponse('please use GET method')


def conference_manager_login(request):
    """
    # Auther: 李东阳
    # 会议室管理员登录
    :param request:
    :return:
    """
    if request.method == 'GET':
        # 校验登录状态
        # 1.校验session是否存在
        if request.session.get('manageraccount') and request.session.get('managerid'):
            # return HttpResponse('{}登录功'.format(request.session.get('username')))
            return HttpResponseRedirect('conference_room/success.html')  # 302 直接跳转到登录成功后的页面
        # 获取浏览器发送过来的cookies
        c_manageraccount = request.COOKIES.get('manageraccount')
        c_managerid = request.COOKIES.get('managerid')
        # 2.校验cookies是否存在，如cookies存在则回写session,for next time
        if c_manageraccount and c_managerid:
            request.session['manageraccount'] = c_manageraccount
            request.session['managerid'] = c_managerid
            # return HttpResponse('已登录')
            return render(request, 'conference_room/success.html')  # 302 直接跳转到登录成功后的页面
        return render(request, 'conference_room/login_manager.html')  # 返回管理员登录页面
    elif request.method == 'POST':
        manager_account = request.POST['manageraccount']
        manager_pwd = request.POST['managerpwd']

        # 用户名验证
        try:
            user = UserManager.objects.get(useraccount=manager_account)
        except Exception as e:
            print('-- login user error %s' % e)
            return HttpResponse('用户名或密码错误')
        # 用户密码验证
        new_password = pass_md5(manager_pwd)  # 对用户密码进行md5加密
        if user.userpwd != new_password:
            return HttpResponse("用户名或密码错误")
        # 记录登录状态
        request.session['manageraccount'] = manager_account  # 注意：此处的键名需要与注册时存的键名保持一致，以便登录状态校验
        request.session['managerid'] = user.id
        resp = HttpResponse('登录成功！！！')  # 302跳转到登录后的页面
        if 'remember' in request.POST:  # 保存cookies
            resp.set_cookie('manageraccount', manager_account, 3600 * 24 * 3)
            resp.set_cookie('managerid', user.id, 3600 * 24 * 3)
        return resp


def conference_compere_login(request):
    """
    # Author: 李东阳
    # 会议主持人登录
    :param request:
    :return:
    """
    if request.method == 'GET':
        # 校验登录状态
        # 1.校验session是否存在
        if request.session.get('compereaccount') and request.session.get('compereid'):
            # return HttpResponse('{}登录功'.format(request.session.get('username')))
            return HttpResponseRedirect('conference_room/success.html')  # 302 直接跳转到登录成功后的页面
        # 获取浏览器发送过来的cookies
        c_compereaccount = request.COOKIES.get('compereaccount')
        c_compereid = request.COOKIES.get('compereid')
        # 2.校验cookies是否存在，如cookies存在则回写session,for next time
        if c_compereaccount and c_compereid:
            request.session['compereaccount'] = c_compereaccount
            request.session['compereid'] = c_compereid
            # return HttpResponse('已登录')
            return HttpResponse('登录成功！！！')  # 302 直接跳转到登录成功后的页面
        return render(request, 'conference_room/login_host.html')  # 返回管理员登录页面
    elif request.method == 'POST':
        compere_account = request.POST['useraccount']
        compere_pwd = request.POST['userpwd']

        # 用户名验证
        try:
            user = UserCompere.objects.get(useraccount=compere_account)
        except Exception as e:
            print('-- login user error %s' % e)
            return HttpResponse('用户名或密码错误')
        # 用户密码验证
        new_password = pass_md5(compere_pwd)  # 对用户密码进行md5加密
        if user.userpwd != new_password:
            return HttpResponse("用户名或密码错误")
        # 记录登录状态
        request.session['compereaccount'] = compere_account  # 注意：此处的键名需要与注册时存的键名保持一致，以便登录状态校验
        request.session['compereid'] = user.id
        resp = HttpResponse('登录成功！！！')  # 302跳转到登录后的页面
        if 'remember' in request.POST:  # 保存cookies
            resp.set_cookie('compereaccount', compere_account, 3600 * 24 * 3)
            resp.set_cookie('compereid', user.id, 3600 * 24 * 3)
        return resp


def manager_register(request):
    if request.method == 'GET':
        return render(request, '')
    elif request.method == 'POST':
        manager_account = request.POST['manageraccount']
        manager_pwd_1 = request.POST['managerpwd_1']
        manager_pwd_2 = request.POST['managerpwd_2']

        if manager_account == '' or manager_pwd_1 == '' or manager_pwd_2 == '':
            print("请输入完整用户信息")
            return render(request, '')
        manager = UserManager.objects.filter(useraccount=manager_account).exist()  # 判断用户是否存在
        if manager:
            print('该用户已存在！！！请勿重复注册')
            return HttpResponse('该用户已存在！！！请勿重复注册')
        else:
            if manager_pwd_1 == manager_pwd_2:
                # 将用户的密码进行md5加密
                new_password = pass_md5(manager_pwd_2)  # 对用户密码进行md5加密
                try:
                    UserManager.objects.create(useraccount=manager_account, userpwd=new_password)  # 上传数据库进行注册
                except Exception:
                    print('用户注册失败，请检测网络是否良好！！！')
                    return HttpResponse('用户注册失败，请检测网络是否良好！！！')
                return HttpResponse('用户注册成功！！！')
            else:
                print('两次输入的密码不正确！！！')
                return HttpResponse('两次输入的密码不正确！！！')


from django.http import JsonResponse
from PIL import Image
import io
import base64
import os


def upload_image(request):
    if request.method == 'GET':
        return render(request, 'conference_room/video.html')
    if request.method == 'POST':
        image_data = request.POST.get('image')
        if image_data:
            image_format, image_str = image_data.split(';base64,')
            ext = image_format.split('/')[-1]
            image = Image.open(io.BytesIO(base64.b64decode(image_str)))
            image.save(f'images/{request.user.username}_{int(time.time())}.{ext}')
            return JsonResponse({'status': 'success', 'message': '图片上传成功'})
        else:
            return JsonResponse({'status': 'error', 'message': '图片数据为空'})
    else:
        return JsonResponse({'status': 'error', 'message': '请求方法错误'})
