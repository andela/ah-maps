# import jwt
#
# from django.conf import settings
#
from rest_framework import authentication, exceptions
#
# from .models import User


class JWTAuthentication(authentication.BaseAuthentication):

    def authenticate(self, request):
        pass
