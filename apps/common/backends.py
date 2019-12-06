from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework.authentication import BaseAuthentication


def get_token(request):
    authorization = request.META.get('HTTP_AUTHORIZATION', "")
    return authorization.split(" ")[-1]


class CustomAuthentication(BaseAuthentication):
    token = None

    def authenticate(self, request, **kwargs):
        if get_token == settings.SECRET_KEY:
            print('U are logged in!!!!!!')
