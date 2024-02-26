from django.urls import path
from .views import CreateBlogView,BlogListView,CategoryView
from rest_framework.routers import DefaultRouter


router=DefaultRouter()
router.register('blog',BlogListView,basename='blog')
app_name="BlogApi"
urlpatterns = [
   path("create/",CreateBlogView.as_view(),name="create_blog"),
   path("category/",CategoryView.as_view(),name='category')
]
urlpatterns+=router.urls