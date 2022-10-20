from django.urls import path
from .views import (
    CategoryView, 
    PostView,
    PostDetailView,
    CommentView, 
    PostUserView
)

urlpatterns = [
    path("category/", CategoryView.as_view()),
    path("posts/", PostView.as_view()), 
    path("posts/<str:slug>/", PostDetailView.as_view()),
    path("posts/<str:slug>/comments/", CommentView.as_view()), 

]