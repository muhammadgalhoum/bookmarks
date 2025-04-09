import os, shutil, logging
from django.utils import timezone
from django.conf import settings
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from django.db.models.signals import post_delete


logger = logging.getLogger(__name__)


@receiver(post_delete, sender=get_user_model())
def delete_user_folders(sender, instance, **kwargs):

    user_directories = [
        os.path.join(settings.MEDIA_ROOT, 'bookmarked_images', instance.username),
        os.path.join(settings.MEDIA_ROOT, 'users_images', instance.username)
    ]

    for user_folder in user_directories:
        if os.path.exists(user_folder):
            try:
                logger.info(
                    f"Attempting to delete folder for user {instance.username}: {user_folder}, Time {timezone.now()}")

                shutil.rmtree(user_folder)

                logger.info(
                    f"Successfully deleted folder for user {instance.username}: {user_folder}, Time {timezone.now()}")
            except Exception as e:
                logger.error(
                    f"Error deleting folder {user_folder} for user {instance.username}: {e}, Time {timezone.now()}")
        else:
            logger.warning(
                f"Folder for user {instance.username} does not exist: {user_folder}, Time {timezone.now()}")
