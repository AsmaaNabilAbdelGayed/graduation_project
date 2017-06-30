from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class UserAccount(models.Model):
    user = models.OneToOneField(User)
    username = models.CharField(max_length=100)
    email = models.CharField(max_length=200)
    password = models.CharField(max_length=50)



    def __str__(self):
        return self.username
