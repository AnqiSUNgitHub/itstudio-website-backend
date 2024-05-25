from django.shortcuts import render,HttpResponse

# Create your views here.
from django.http import Http404
from django.core.mail import send_mail
import random, re

EMAIL_RE = re.compile(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$')

def send(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if EMAIL.match(email) is None:
            return Http404("邮箱错误")
        print(email)
        global code  #全局变量，用于后续注册验证匹配
        code = '%08d' % random.randint(0, 99999999)
        print(code)
        msg = "您的验证码是" + code + ",10分钟内有效，请尽快填写"
        print(msg)
        send_status = send_mail('找回密码验证', msg, '954569093@qq.com', [email])
        print(send_status)
        return HttpResponse(status=200)
