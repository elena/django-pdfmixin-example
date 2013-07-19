from django.db import models

class Page(models.Model):
    title = models.CharField(max_length=30)
    slug = models.SlugField()

