from rest_framework import serializers
from ...models import Blog,Category
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields=['title']

class CreateBlogSerializer(serializers.ModelSerializer):
    author=serializers.CharField(read_only=True)
    categories=CategorySerializer(read_only=True,many=True)

    class Meta:
        model=Blog
        fields=['id','author','title','categories','shortdescription','body','image','create_date','expire_date']


class BlogListSerializer(CreateBlogSerializer): 

    def to_representation(self, instance):

        rep=super().to_representation(instance)
        request=self.context.get('request')    
        if not request.parser_context.get("kwargs").get("pk"):
            rep.pop('body')
            return rep
        return rep


