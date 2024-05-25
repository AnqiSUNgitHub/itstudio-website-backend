
import random, re
import smtplib  # for error handle

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.core.mail import send_mail

EMAIL_RE = re.compile(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$')

@require_http_methods(['POST'])
def send(request):
    email = request.POST.get('email')
    if EMAIL_RE.match(email) is None:
        return JsonResponse(dict(detail="邮箱格式错误"), status=422)
    print(email)
    global code  #全局变量，用于后续注册验证匹配
    code = '%08d' % random.randint(0, 99999999)
    print(code)
    msg = "您的验证码是" + code + ",10分钟内有效，请尽快填写"
    print(msg)
    num_sent = 0
    err_msg = "success"
    try:
        num_sent = send_mail('找回密码验证', msg, '954569093@qq.com', [email])
    except smtplib.SMTPServerDisconnected:
        err_msg = "SMTP server disconnected"
    except smtplib.SMTPResponseException as e:
        err_msg = e.smtp_error
        assert type(err_msg) is str
    except smtplib.SMTPException as e:
        err_msg = "error"
    
    print(num_sent)
    if num_sent == 0:  # zero email has been sent
        return JsonResponse(dict(detail=err_msg) , status=500)
    else:
        return JsonResponse(status=200)

