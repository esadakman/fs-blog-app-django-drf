from rest_framework import serializers
from .models import Category, Post,  Like, Comment, View


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            "id",
            "name"
        )


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = (
            "id",
            "content",
            "time_stamp",
            "user",
        )


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

    
    class Meta:
        model = Post
        fields = (
            "id",
            "title",
            "author",
            "category", 
            "content",
            "post_image",
            "date_posted",  
            "slug",
            "view_count",
            "post_comment",
            "comment_count",
            "post_like",
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
        return View.objects.filter(post=obj.id).count()