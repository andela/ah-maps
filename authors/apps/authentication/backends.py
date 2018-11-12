import jwt
#
from django.conf import settings
#
from rest_framework import authentication, exceptions
#
from .models import User


class JWTAuthentication(authentication.BaseAuthentication):

    keyword = "Bearer"

    def authenticate(self, request):
        """
        This checks that the passed JWt token is valid and returns a user and his/her token on successful verification.
        """

        request.user = None

        # returns Authorization header as a bytestring


        auth_header = authentication.get_authorization_header(request).split()

        if not auth_header or auth_header[0].decode().lower() != self.keyword.lower():
            return None

        if len(auth_header) == 1:
            raise exceptions.AuthenticationFailed('Invalid token header. No credentials provided.')
        elif len(auth_header) > 2:
            raise exceptions.AuthenticationFailed('Invalid token header. Token string should not spaces.')
        return self.authenticate_credentials(request, auth_header[1].decode())

    def authenticate_credentials(self, request, token):
        """
        authenticate given credentials. If authentication is successful,
        return the user and token. If not, return an error.
        """
        try:
            payload = jwt.decode(token, settings.SECRET_KEY)
        except Exception as e:
            if e.__class__.__name__ == 'DecodeError':
                raise exceptions.AuthenticationFailed('Cannot decode token')
            elif e.__class__.__name__ == "ExpiredSignatureError":
                raise exceptions.AuthenticationFailed('Token has expired')
            else:
                raise exceptions.AuthenticationFailed(str(e))

        try:
            user = User.objects.get(pk=payload['id'])
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('No user found!')
        if not user.is_active:
            raise exceptions.AuthenticationFailed('User has been deactivated')
        return user, payload

    def authenticate_header(self, request):
        return self.keyword
