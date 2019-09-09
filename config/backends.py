import logging

from django.contrib.auth import get_user_model
from rest_framework import authentication, exceptions
from smeApi_auth.models import ApiKey


User = get_user_model()
LOGGER = logging.getLogger(__name__)


class APIKEYBackend(authentication.BaseAuthentication):
    """
    Authenticate against api key
    """

    def authenticate(self, request):
        """get the use via api key"""
        auth = request.META.get('HTTP_AUTHORIZATION', '').split()

        if len(auth) != 2:
            raise exceptions.AuthenticationFailed(
                'Invalid authorization header.')

        key = auth[1]

        try:
            api_key = ApiKey.objects.get(key=key)
            return (api_key.user, None)
        except ApiKey.DoesNotExist:
            raise exceptions.AuthenticationFailed('Invalid Api Key.')

    def get_user(self, user_id):
        try:
            user = User.objects.get(pk=user_id)
            if user.is_active:
                return user
            return None
        except User.DoesNotExist:
            return None


class EmailOrUsernameModelBackend(object):
    """
    Simple backend to allow users to log in with their email or
    their username in auth forms
    """

    def authenticate(self, username=None, password=None):
        if '@' in username:
            kwargs = {'email': username}
        else:
            kwargs = {'username': username}
        try:
            user = User.objects.get(**kwargs)
            if user.check_password(password):
                return user
            return None
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
