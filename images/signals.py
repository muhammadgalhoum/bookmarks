from django.dispatch import receiver
from django.db.models.signals import m2m_changed
from.models import Image

@receiver(m2m_changed, sender=Image.liked_by.through)
def liked_by_changed(sender, instance, **kwargs):
    instance.total_likes = instance.liked_by.count()
    instance.save()

