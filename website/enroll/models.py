from django.db import models

class VerifyCodeModel(models.Model):
    email = models.EmailField(unique=True)
    code = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)

class EnrollmentModel(models.Model):
    PROGRESS_CHOICES = (
        ('已提交', '已提交'),
        ('审核中', '审核中'),
        ('已通过', '已通过'),
        ('已拒绝', '已拒绝'),
    )

    email = models.EmailField()
    verification_code = models.CharField(max_length=10)
    progress = models.CharField(choices=PROGRESS_CHOICES, default='已提交', max_length=10)
