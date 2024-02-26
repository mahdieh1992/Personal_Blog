from django.urls import path,include

app_name="Blog"
urlpatterns = [
   path("api/v1/",include("Blog.api.v1.urls"),name="api")
]