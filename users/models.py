from django.db import models
from django.contrib.auth.models import User  
class UserModel(User):
    @property
    def my_profile(self):
        return self.profile


class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='profile')
    
    image = models.URLField(max_length=300, blank=True,
                            default="https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_1280.png") 

    def __str__(self):
        return f"{self.user.username} Profile"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs) 