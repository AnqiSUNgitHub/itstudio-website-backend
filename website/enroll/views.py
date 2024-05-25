
import random, re

from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
if settings.DEBUG:
    def log(*a): print(*a)
else:
    def log(*_): pass
from .models import VerifyCodeModel
from .verify_code import send_code

EMAIL_RE = re.compile(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$')

def gen_code() -> str:
    code = '%08d' % random.randint(0, 99999999)
    return code

@csrf_exempt
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

    err_msg = send_code(code, [email])
    if err_msg is None:
        return JsonResponse(data={}, status=200)
    else:
        return JsonResponse(dict(detail=err_msg) , status=500)

