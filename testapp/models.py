from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class UserModel(AbstractUser):
    username = models.CharField(max_length=16, unique=True)
    first_name = models.CharField(max_length=16, blank=True)
    last_name = models.CharField(max_length=16, blank=True)
    date_joined = models.DateTimeField(null=True)
    photo_url = models.URLField(blank=True, max_length=255)

    def __str__(self):
        return self.username



