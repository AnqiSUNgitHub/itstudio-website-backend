import json
import random, datetime

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

    email = json.loads(request.body.decode('utf-8')).get('email', None)
    if email is None:
        return JsonResponse(dict(detail="email is required but missing"), status=422)
    log(email)
    obj = VerifyCodeModel.objects.filter(email=email).first()
    code = gen_code()
    def create_new():
        nonlocal obj
        try:
            obj = VerifyCodeModel.objects.create(email=email, code=code)
        except ValidationError:
            return JsonResponse(dict(detail="邮箱格式错误"), status=422)
    
    if obj is not None:
        ddl = datetime.datetime.now()-datetime.timedelta(minutes=10)
        if obj.send_time < ddl:
            obj.delete()
            res = create_new()
            if res is not None:
                return res
        obj.code = code
    else:
        res = create_new()
        if res is not None:
            return res
    obj.save()

    log(code)

    err_msg = send_code(code, [email])
    if err_msg is None:
        return JsonResponse(data={}, status=200)
    else:
        return JsonResponse(dict(detail=err_msg) , status=500)

