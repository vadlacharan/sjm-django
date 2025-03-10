from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from django.utils.text import slugify

class User(models.Model):
    
    def __str__(self):
        return self


class Publication(models.Model):
    title = models.CharField(max_length=300)
    url = models.URLField(blank=True, null=True)
    abstract = models.TextField()
    description = models.TextField()
    likes =models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=300,unique=True, blank=True, default="", editable=False)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class Comment(models.Model):
    user_id = models.IntegerField()
    publication_id = models.IntegerField()
    comment_value = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Likes(models.Model):
    user_id = models.IntegerField()
    publication_id=models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

class Saved(models.Model):
    user_id = models.IntegerField()
    publication_id=models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

class News(models.Model):
    text = models.TextField()  # The announcement text
    created_at = models.DateTimeField(auto_now_add=True)  # When the announcement was created

    def __str__(self):
        return self.text[:50]

