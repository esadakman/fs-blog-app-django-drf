from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response 
from .models import Category, Post, Like, Comment, View
from .serializers import (
    CategorySerializer,
    PostSerializer,
    LikeSerializer,
    CommentSerializer,
)
from rest_framework import permissions
from .permissions import IsAdminOrReadOnly, IsAuthorOrReadOnly

# Create your views here.


class CategoryView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]


class PostView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = "slug"
    permission_classes = [IsAuthorOrReadOnly]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        View.objects.create(user=request.user, post=instance)
        return Response(serializer.data)


class CommentView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        slug = self.kwargs.get('slug')
        blog = get_object_or_404(Post, slug=slug)
        user = self.request.user
        comments = Comment.objects.filter(blog=blog, user=user)
        serializer.save(blog=blog, user=user)
