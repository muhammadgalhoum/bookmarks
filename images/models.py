import os, datetime
from django.db import models
from django.conf import settings
from django.utils.text import slugify


def user_directory_path(instance, filename):
    return os.path.join(
        'bookmarked_images',
        instance.user.username,
        datetime.datetime.now().strftime('%Y/%m/%d'), 
        filename)
    
    
class Image(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='images',
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, blank=True, unique_for_date='created')
    url = models.URLField(max_length=2000)
    image = models.ImageField(upload_to=user_directory_path)
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    liked_by = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_images', blank=True)
    total_likes = models.PositiveIntegerField(default=0)
    
    class Meta:
        indexes = [
            models.Index(fields=['-created']),
            models.Index(fields=['-total_likes']),
        ]
        ordering = ['-created']
        
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title
