from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from upload.models import Image

class ImageForm(forms.ModelForm):
    product = forms.ImageField()

    class Meta:
        model = Image
        exclude = ('userid',)
