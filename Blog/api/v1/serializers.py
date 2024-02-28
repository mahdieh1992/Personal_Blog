from rest_framework import serializers
from ...models import Blog, Category, Comment


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.CharField(read_only=True)

    class Meta:
        model = Comment
        fields = ["blog", "author", "body", "create_date", "parent"]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "title"]


class CreateBlogSerializer(serializers.ModelSerializer):
    author = serializers.CharField(read_only=True)

    class Meta:
        model = Blog
        fields = [
            "id",
            "author",
            "title",
            "categories",
            "shortdescription",
            "body",
            "image",
            "create_date",
            "expire_date"
        ]


class BlogListSerializer(CreateBlogSerializer):

    def to_representation(self, instance):

        rep = super().to_representation(instance)
        rep["categories"] = CategorySerializer(
            instance.categories, many=True
        ).data
        rep["comment"] = CommentSerializer(instance.comment, many=True).data
        request = self.context.get("request")
        if not request.parser_context.get("kwargs").get("pk"):
            rep.pop("body")
            return rep
        return rep
