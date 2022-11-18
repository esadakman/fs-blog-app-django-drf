from django.db import models
from django.conf import settings
from django.utils import timezone 
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
        User,  on_delete=models.CASCADE,  related_name="post_author",)
    # default='Anonymous User', 
    date_posted = models.DateTimeField(default=timezone.now)
    category = models.ForeignKey(
        Category, related_name="post_category", on_delete=models.CASCADE)
    post_image = models.URLField(max_length=300, blank=True,
                                 default="https://www.mericity.com/resources/images/Default.jpg")
    slug = models.SlugField(blank=True, unique=True)
    blog_comment = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ('-date_posted',)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class Like(models.Model):
    post = models.ForeignKey(
        Post, related_name="post_likes", on_delete=models.CASCADE)
    user = models.ForeignKey(
        User, related_name="liked_user", on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.user.username


class Comment(models.Model):
    user = models.ForeignKey(
        User, related_name="comment_user", on_delete=models.CASCADE, null=True)
    blog = models.ForeignKey(
        Post, related_name="post_comment", on_delete=models.CASCADE)
    content = models.TextField()
    time_stamp = models.DateTimeField(auto_now_add=True, blank=True)

    

    def __str__(self):
        return f"Commented by {self.user} to {self.blog} "


class View(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    time_stamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} viewed {self.post} "
