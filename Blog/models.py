from django.db import models
import datetime
from django.contrib.auth import get_user_model

year = 2025
month = 12
get_date = datetime.date(year, month, 29)

user = get_user_model()


class Blog(models.Model):
    author = models.ForeignKey(
        user, on_delete=models.CASCADE, related_name="blog"
    )
    categories = models.ManyToManyField("Category", related_name="blog")
    title = models.CharField(max_length=100)
    shortdescription = models.CharField(max_length=250)
    body = models.TextField()
    image = models.ImageField(upload_to="Image/blog", blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    create_date = models.DateTimeField(auto_now_add=True)
    expire_date = models.DateField(default=get_date)
    modify_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title}"


# Create your models here.


class Category(models.Model):
    title = models.CharField(max_length=200)

    def __str__(self) -> str:
        return f"{self.title}"


class Comment(models.Model):
    blog = models.ForeignKey(
        Blog, on_delete=models.CASCADE, related_name="comment"
    )
    author = models.ForeignKey(
        user, on_delete=models.CASCADE, related_name="comment"
    )
    body = models.TextField()
    create_date = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="reply",
    )
    reply_count = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.author.email} {self.blog}"

    def children(self):
        return Comment.objects.filter(parent=self)

    @property
    def is_parent(self):
        if self.parent is not None:
            return False
        return True
