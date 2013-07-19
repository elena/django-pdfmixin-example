from django.db import models
from django.contrib import admin

class Page(models.Model):
    title = models.CharField(max_length=30)
    slug = models.SlugField()


admin.site.register(Page)