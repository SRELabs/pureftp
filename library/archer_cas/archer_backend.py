from django.contrib.auth.models import User


class ArcherBackend:
    def __init__(self):
        pass

    @staticmethod
    def authenticate(username=None, password=None):
        if username:
            try:
                user = User.objects.get(username=username)
                return user
            except User.DoesNotExist:
                pass
        return None

    @staticmethod
    def get_user(user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
