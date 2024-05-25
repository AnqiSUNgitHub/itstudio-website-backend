
import random, re
import smtplib  # for error handle

from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.core.mail import send_mail
from django.conf import settings
if settings.DEBUG:
    def log(*a): print(*a)
else:
    def log(*_): pass
from .models import VerifyCodeModel

EMAIL_RE = re.compile(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$')

def gen_code() -> str:
    code = '%08d' % random.randint(0, 99999999)
    return code

@require_http_methods(['POST'])
def send(request):
    email = request.POST.get('email')
    log(email)
    obj = VerifyCodeModel.objects.filter(email=email).first()
    code = gen_code()
    if obj is not None:
        obj.code = code
    else:
        try:
            obj = VerifyCodeModel.objects.create(email=email, code=code)
        except ValidationError:
            return JsonResponse(dict(detail="邮箱格式错误"), status=422)
    obj.save()

    log(code)
    msg = "您的验证码是" + code + ",10分钟内有效，请尽快填写"
    log(msg)
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
    
    log(num_sent)
    if num_sent == 0:  # zero email has been sent
        return JsonResponse(dict(detail=err_msg) , status=500)
    else:
        return JsonResponse(status=200)

