import random
import redis
from django.shortcuts import render
from django.http.response import HttpResponse
from django.urls import reverse

from door_visits.models import User

# Create your views here.
r = redis.Redis(host='43.140.200.240', port=6379, password='team2111.', db=6)


def ewm_view(request):
    """
    # auther: 李东阳
    用户申请访客视图函数
    :param request:
    :return:
    """
    if request.method == 'GET':  # get请求得到访客页面
        return render(request, 'door_visits/visits.html')
    if request.method == 'POST':  # post请求生成二维码
        user_name = str(request.POST['user name'])  # 获取用户输入的用户名
        phone = str(request.POST['user phone'])  # 获取用户输入的手机号
        if phone == "" or user_name == "":   # 判断用户是否输入信息
            return render(request, 'door_visits/visits.html')
        else:
            try:
                user = User.objects.get(username=user_name)
                user_phone = user.userphone
            except Exception:
                print('该用户不存在')
                return render(request, 'door_visits/visits.html')
            if user_phone == phone:  # 判断用户的手机号是否正确
                random.seed()
                new_int = str(random.randint(100000, 999999))
                phone += str(new_int)
                r.set(user_name, phone)
                r.expire(user_name, 60)  # redis设置过期时间为60秒
                create_qr(phone)  # 调用生成二维码函数
                image_url = reverse('image_view')  # 获取二维码
                context = {
                    'user_name': user_name,
                    'image_url': image_url,
                }
                return render(request, 'door_visits/both.html', context)
            else:
                return render(request, 'door_visits/visits.html')


def update_qr(request, username):
    """
    # Auther: 李东阳
    更新二维码视图函数
    :param request:
    :param username:
    :return:
    """
    user = User.objects.filter(username=username)
    userphone = str(user[0].userphone)
    random.seed()
    new_int = str(random.randint(100000, 999999))
    userphone += new_int
    r.set(username, userphone)
    r.expire(username, 60)  # redis设置过期时间为60秒
    create_qr(userphone)  # 调用生成二维码函数
    image_url = reverse('image_view')  # 获取二维码
    context = {
        'user_name': username,
        'image_url': image_url,
    }
    return render(request, 'door_visits/both.html', context)


def image_view(request):
    """
    # Auther: 李东阳
    # 读取图片文件
    :param request:
    :return:
    """
    with open(r"2.png", 'rb') as f:
        image_data = f.read()

    # 返回图片数据
    return HttpResponse(image_data, content_type='image/png')


def create_qr(scc):
    """
    # Auther:李东阳
    创建二维码
    :param scc:
    :return:
    """
    import qrcode
    # QRCode（）这里我们创建了一个对象：
    qr = qrcode.QRCode(version=5, error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=8, border=4)
    # 向二维码中添加信息
    qr.add_data(scc)

    qr.make(fit=True)

    img = qr.make_image()
    # 二维码设置为彩色
    img = img.convert('RGBA')
    img.save('2.png')
