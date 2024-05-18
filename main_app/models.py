from django.db import models
from datetime import date

from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.URLField()
    # hunt_instance = models.ManyToManyField()#hunt_instance

    def __str__(self) -> str:
        return self.user.username
    
