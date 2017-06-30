from django.db import models
from django.contrib.auth.models import User

class Image(models.Model):
    userid = models.ForeignKey(User)
    product = models.ImageField(upload_to='media')

