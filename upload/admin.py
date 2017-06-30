from django.contrib import admin
from .models import Image





class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'userid','product']


admin.site.register(Image)