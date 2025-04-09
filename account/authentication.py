import logging
from django.utils import timezone
from django.contrib.auth import get_user_model


logger = logging.getLogger(__name__)


class EmailAuthBackend:
    """
    Authenticate using an e-mail address.
    """
    UserModel = get_user_model()

    def authenticate(self, request, username=None, password=None):
        try:
            user = self.UserModel.objects.get(email=username)
            if user.check_password(password):
                return user
            return None
        except self.UserModel.DoesNotExist:
            logger.debug(
                f"Login attempt for non-existent email: {username}, Time {timezone.now()}")
            return None
        except self.UserModel.MultipleObjectsReturned:
            logger.critical(f"Multiple users with email: {username} (DB INCONSISTENCY), Time at {timezone.now()}")
            return None

    def get_user(self, user_id):
        try:
            return self.UserModel.objects.get(pk=user_id)
        except self.UserModel.DoesNotExist:
            return None
        