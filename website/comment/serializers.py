from rest_framework import serializers


class commentSerializer(serializers.Serializer):
    id = serializers.IntegerField(label="id")
    comment_time = serializers.DateTimeField(label='datetime')
    content = serializers.CharField(label='comment')
