from rest_framework import serializers
from .models import Category, Post,  Like, Comment, View
from users.serializers import ProfileUpdateForm
from django.utils.timezone import now

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            "id",
            "name"
        )


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    user_pp = serializers.CharField(
        source="user.profile.image", read_only=True) 

    class Meta:
        model = Comment
        fields = (
            "id",
            "content",
            "time_stamp",
            "user",
            "user_pp",  
        )
        # fields = '__all__'


class LikeSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    user_id = serializers.IntegerField()

    class Meta:
        model = Like
        fields = (
            "id",
            "user",
            "user_id",
            "post"
        )


class PostSerializer(serializers.ModelSerializer):
    post_comment = CommentSerializer(many=True, read_only=True)
    post_like = LikeSerializer(many=True, read_only=True)
    like_count = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()
    view_count = serializers.SerializerMethodField()
    author_id = serializers.CharField(
        source="author.id", read_only=True) 
    author = serializers.StringRelatedField(read_only=True) 
    author_pp =  serializers.CharField(
        source="author.profile.image", read_only=True)
    category_name =  serializers.CharField(
        source="category", read_only=True)

    class Meta:
        model = Post
        # fields = '__all__'
        fields = (
            "id",
            "title",
            "author",
            "author_id",
            "author_pp",
            "category", 
            "category_name", 
            "content",
            "post_image",
            "date_posted",
            "slug",
            "post_comment",
            "post_like",
            "comment_count",
            "view_count",
            "like_count",
        )
        read_only_fields = (
            "date_posted",
            "slug",
        )

    def get_like_count(self, obj):
        return Like.objects.filter(post=obj.id).count()

    def get_comment_count(self, obj):
        return Comment.objects.filter(blog=obj.id).count()

    def get_view_count(self, obj):
        # print(len(set(View.objects.filter(post=obj.id))), 'asd')s
        return View.objects.filter(post=obj.id).count()
