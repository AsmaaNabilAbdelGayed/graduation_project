from __future__ import unicode_literals
from django.db import models


class ImageClass(models.Model):
    class_name= models.CharField(max_length=255)

    def __str__(self):
        return self.class_name


class LabelsClass(models.Model):
    label_name= models.CharField(max_length=255)

    def __str__(self):
        return self.label_name



class Photo(models.Model):
    class_name = models.ForeignKey(ImageClass, on_delete=models.CASCADE)
    label_name = models.ManyToManyField(LabelsClass)
    name = models.CharField(max_length=255)
    photo = models.ImageField(upload_to='./photos/')
    features = models.FileField(blank = True , upload_to= './features/')
    price = models.DecimalField(max_digits=10, decimal_places=2,default = 100)

    def __str__(self):
        return self.name


