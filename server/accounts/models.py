from django.contrib.auth.models import AbstractUser
from django.db import models
# Create your models here.


class User(AbstractUser):
    profile_image = models.ImageField(null=True ,blank=True)
    followings = models.ManyToManyField('self', symmetrical=False, related_name='followers')
    intro = models.TextField(null=True)