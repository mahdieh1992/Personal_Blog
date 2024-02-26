from django.db import models
from datetime import date,timezone
from django.contrib.auth import get_user_model

get_date=date.today()
year_add=get_date.year + 2
get_date=get_date.replace(year=year_add)

user=get_user_model()



class Blog(models.Model):
    author=models.ForeignKey(user,on_delete=models.CASCADE,related_name='blog')
    categories=models.ManyToManyField("Category",related_name='blog')
    title=models.CharField(max_length=100)
    shortdescription=models.CharField(max_length=250)
    body=models.TextField()
    image=models.ImageField(upload_to='Image/blog',blank=True,null=True)
    is_deleted=models.BooleanField(default=False)
    create_date=models.DateTimeField(auto_now_add=True)
    expire_date=models.DateField(default=get_date)
    modify_date=models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title}"
# Create your models here.


class Category(models.Model):
    title=models.CharField(max_length=200)

    def __str__(self) -> str:
        return f"{self.title}"