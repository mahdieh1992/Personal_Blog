from django.urls import path
from .views import CreateBlogView, BlogListView, CategoryView, CommentView
from rest_framework.routers import DefaultRouter

app_name = "BlogApi"
router = DefaultRouter()
router.register("blog", BlogListView, basename="blog")


urlpatterns = [
    path("create/", CreateBlogView.as_view(), name="create_blog"),
    path(
        "category/",
        CategoryView.as_view(
            {"get": "list", "post": "create", "put": "update"}
        ),
        name="category",
    ),
    path(
        "category/<int:pk>/",
        CategoryView.as_view({"put": "update"}),
        name="category_id",
    ),
    path("comment/", CommentView.as_view({"get": "list"}), name="list"),
    path(
        "comment/<int:pk>/",
        CommentView.as_view({"post": "create"}),
        name="create",
    ),
]
urlpatterns += router.urls
