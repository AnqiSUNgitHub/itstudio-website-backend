import json
import random , datetime

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

def gen_code() -> str:
    code = '%04d' % random.randint(1000, 9999)
    return code

@csrf_exempt
@require_http_methods(['POST'])
def send(request):
    email = request.POST.get('email')
    email=json.loads(email)
    log(email)
    obj = VerifyCodeModel.objects.filter(email=email).first()
    code = gen_code()
    send_time=datetime.datetime.now()
    if obj is not None:
        obj.code = code
    else:
        try:
            obj = VerifyCodeModel.objects.create(email=email, code=code,send_time=send_time)
        except ValidationError:
            return JsonResponse(dict(detail="邮箱格式错误"), status=422)
    obj.save()

    log(code)

    err_msg = send_code(code, [email])
    VerifyCodeModel.objects.filter(
        send_time=datetime.datetime.now()-datetime.timedelta(minutes=10)).delete()#清除间隔发送时间10分钟的数据
    if err_msg is None:
        return JsonResponse(data={}, status=200)
    else:
        return JsonResponse(dict(detail=err_msg) , status=500)

