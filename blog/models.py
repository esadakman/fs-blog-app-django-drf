from django.db import models
from django.conf import settings
from django.utils import timezone
from PIL import Image
# Create your models here.
User = settings.AUTH_USER_MODEL


class Category(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Post(models.Model): 
    title = models.CharField(max_length=100)
    content = models.TextField()
    author = models.ForeignKey(
        User,  on_delete=models.CASCADE, default='Anonymous User', related_name="post_author",) 
    date_posted = models.DateTimeField(default=timezone.now)
    category = models.ForeignKey(
        Category, related_name="post_category", on_delete=models.CASCADE)
    post_image = models.ImageField(
        default="blog_default.png", upload_to="blog_pics") 
    slug = models.SlugField(blank=True, unique=True)
    blog_comment = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title


    def save(self, *args, **kwargs):  
        super().save(*args, **kwargs)

        img = Image.open(self.post_image.path)

        if img.height > 300 or img.width > 300:
            output_size = (400, 400)
            img.thumbnail(output_size)
            img.save(self.post_image.path)


class Like(models.Model):
    post = models.ForeignKey(Post, related_name="post_likes", on_delete=models.CASCADE)
    user = models.ForeignKey(
        User, related_name="liked_user", on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.user.username

class Comment(models.Model):
    user = models.ForeignKey(
        User, related_name="comment_user", on_delete=models.CASCADE, null=True)
    blog = models.ForeignKey(Post, related_name="post_comment", on_delete=models.CASCADE)
    content = models.TextField()
    time_stamp = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return f"Commented by {self.user} to {self.blog} "

class View(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    time_stamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.user.username