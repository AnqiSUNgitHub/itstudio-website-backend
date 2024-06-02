from django.shortcuts import render
from django.http import JsonResponse
from .models import VerifyCodeModel, EnrollmentModel
from django.views.decorators.csrf import csrf_exempt
import random
import string

@csrf_exempt
def enroll(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        code = request.POST.get('code')

        
        try:
            verify_code = VerifyCodeModel.objects.get(email=email, code=code)
        except VerifyCodeModel.DoesNotExist:
            return JsonResponse({'message': '验证码错误'}, status=400)

       
        enrollment = EnrollmentModel.objects.create(email=email, verification_code=code)

        return JsonResponse({'message': '报名成功'}, status=201)

    return JsonResponse({'message': '只允许POST请求'}, status=405)

