import os, datetime, uuid
from django.db import models
from django.urls import reverse
from django.conf import settings
from django.utils.text import slugify
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError

    
class Contact(models.Model):
    user_from = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='following_set',
        on_delete=models.CASCADE,
        null=False,
        blank=False,
    )
    
    user_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='follower_set',
        on_delete=models.CASCADE,
        null=False,
        blank=False,
    )
    
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        # Prevent duplicate relationships
        unique_together = ('user_from', 'user_to')       
        indexes = [
            models.Index(fields=['-created']),
        ]        
        ordering = ['-created']
        
    def clean(self):
        if self.user_from_id is None:
            raise ValidationError("user_from field is required.")
        if self.user_to_id is None:
            raise ValidationError("user_to field is required.")
        if self.user_from_id == self.user_to_id:
            raise ValidationError("Users cannot follow themselves.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
        
    def __str__(self):
        return f"{self.user_from} follows {self.user_to}"


def user_directory_path(instance, filename):
    return os.path.join(
        'users_images',
        instance.username,
        datetime.datetime.now().strftime('%Y/%m/%d'),
        filename)


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to=user_directory_path, blank=True)
    following = models.ManyToManyField('self', through=Contact, related_name='followers', symmetrical=False)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    slug = models.SlugField(max_length=50, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.username)
        super().save(*args, **kwargs)
        
    def get_absolute_url(self):
        return reverse("account:user_detail", kwargs={"slug": self.slug, "uuid": self.uuid})
    