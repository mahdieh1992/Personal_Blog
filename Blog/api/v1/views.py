from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from rest_framework import viewsets
from .serializers import (
    CreateBlogSerializer,
    BlogListSerializer,
    CategorySerializer,
    CommentSerializer,
)
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework import status
from django.contrib.auth import get_user_model
from ...models import Blog, Category, Comment
from rest_framework.decorators import action
from .pagination import ResultPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie

user = get_user_model()


class CreateBlogView(CreateAPIView):
    """
    create new blog if user access is admin and isAuthenticated
    """

    serializer_class = CreateBlogSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=self.request.user)
            return Response(
                {"detail": serializer.data}, status=status.HTTP_201_CREATED
            )
        return Response(
            {"detail": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
        )


class BlogListView(viewsets.ModelViewSet):
    """
    we used of BlogListView class for show list of objects
    Show details of each object
    Delete object by Admin site
    Edit Object
    """

    serializer_class = BlogListSerializer
    pagination_class = ResultPagination
    filter_backends = [OrderingFilter, SearchFilter, DjangoFilterBackend]
    filterset_fields = ["categories"]
    search_fields = ["title"]
    ordering_fields = ["create_date"]

    def get_permissions(self):
        permission_classes = [IsAuthenticated]
        if self.action in ["list", "retrieve"]:
            permission_classes = [IsAuthenticated]
        elif self.action in ["destroy", "update"]:
            permission_classes = [IsAdminUser]
        return [permission() for permission in self.permission_classes]

    def get_queryset(self):
        blog = Blog.objects.all()
        return blog

    def list(self, request, *args, **kwargs):
        """
        show list of blogs with determine count object in per page
        """
        queryset = self.filter_queryset(self.get_queryset())
        page_data = self.paginate_queryset(
            queryset
        )  # paginate object and get paginated data for per page_number
        if page_data is not None:
            serializer = self.get_serializer(page_data, many=True)
            return self.get_paginated_response(
                serializer.data
            )  # return paginated response object

        serializer = self.get_serializer(queryset, many=True)
        return Response(
            {"detail": serializer.data}, status=status.HTTP_200_OK
        )

    def retrieve(self, request, *args, **kwargs):
        """
        retrieve object if not deleted object
        """

        object = self.get_object()
        if object.is_deleted is False:
            serializer = self.get_serializer(object)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(
            {"detail": "content is not exists"},
            status=status.HTTP_204_NO_CONTENT,
        )

    def destroy(self, request, *args, **kwargs):
        """
        delete object by Admin
        """
        object = self.get_object()
        object.delete()
        return Response(
            {"detail:object is delete successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )

    def update(self, request, *args, **kwargs):
        object = self.get_object()
        serializer = self.serializer_class(object, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryView(viewsets.ModelViewSet):
    """
    create,update and show list of categories
    """

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=["get"])
    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["post"])
    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["put"])
    def update(self, request, *args, **kwargs):
        object = self.get_object()
        serializer = self.get_serializer(object, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(
            {"detail": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
        )


class CommentView(viewsets.ModelViewSet):
    """
    create and show comment
    """

    serializer_class = CommentSerializer
    queryset = Comment.objects.all()

    @action(detail=True, methods=["post"])
    def create(self, request, pk):
        blog_object = get_object_or_404(Blog, id=pk)
        data = self.request.data
        if "parent" in data:
            parent = data["parent"]
        else:
            parent = 0
        body = data.get("body")
        obj = Comment.objects.create(
            author=self.request.user,
            blog=blog_object,
            parent_id=parent,
            body=body,
        )
        serializer = self.get_serializer(obj, data)
        if serializer.is_valid(raise_exception=True):
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @method_decorator(cache_page(60 * 20))
    @method_decorator(vary_on_cookie)
    @action(detail=False, methods=["get"])
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
