from django.contrib import admin
from .models import *
# Register your models here.


class ProductAdmin(admin.ModelAdmin):
    list_display = ['id','pname','pcategory']

admin.site.register(Products,ProductAdmin)