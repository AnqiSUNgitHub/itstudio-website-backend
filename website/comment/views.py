from django.http import JsonResponse
import datetime
from rest_framework.views import APIView
from .models import *
from .serializers import commentSerializer


class CommentView(APIView):
    def get(self):
        comments = comment.objects.filter(parent_id="")
        serializer = commentSerializer(comments, many=True).data
        for i in serializer:
            sub_comment = comment.objects.filter(parent_id=i['id'])
            i['children'] = []
            for j in sub_comment:
                i["children"].append(j.comment_time.isoformat())
                i["children"].append(j.content)
        return JsonResponse(serializer)

    def post(self, request):
        content = request.data.get("content")
        parent_id = request.data.get("parent_id", "")
        flag = comment.objects.filter(parent_id=parent_id)
        if flag:
            if parent_id != "":
                comment.objects.create(content=content, parent_id=parent_id)
            else:
                comment.objects.create(content=content, parent_id="")
            return JsonResponse({'code': 200, 'msg': '成功'}, status=200)
        else:
            return JsonResponse({'code': 404, 'msg': 'parent_id不存在'}, status=404)
