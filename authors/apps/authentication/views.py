import re

from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError
from .backends import JWTAuthentication

from .renderers import UserJSONRenderer
from .serializers import (
    LoginSerializer, RegistrationSerializer, UserSerializer
)
from django.contrib.auth.hashers import check_password

from .models import User

auth = JWTAuthentication()

class RegistrationAPIView(APIView):
    # Allow any user (authenticated or not) to hit this endpoint.
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = RegistrationSerializer

    def post(self, request):
        user = request.data.get('user', {})
        # The create serializer, validate serializer, save serializer pattern
        # below is common and you will see it a lot throughout this course and
        # your own work later on. Get familiar with it.
        serializer = self.serializer_class(data=user, context={"request":request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        success_message = {"success" : "please confirm your email to continue"}

        return Response(success_message, status=status.HTTP_201_CREATED)


class LoginAPIView(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = LoginSerializer

    def post(self, request):
        user = request.data.get('user', {})

        # Notice here that we do not call `serializer.save()` like we did for
        # the registration endpoint. This is because we don't actually have
        # anything to save. Instead, the `validate` method on our serializer
        # handles everything we need.
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UserSerializer

    def retrieve(self, request, *args, **kwargs):
        # There is nothing to validate or save here. Instead, we just want the
        # serializer to handle turning our `User` object into something that
        # can be JSONified and sent to the client.
        serializer = self.serializer_class(request.user)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        serializer_data = request.data.get('user', {})

        # Here is that serialize, validate, save pattern we talked about
        # before.
        serializer = self.serializer_class(
            request.user, data=serializer_data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


class ActivateAPIView(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = LoginSerializer

    def get(self, request, token):
        user = auth.authenticate_credentials(request, token)
        if user.is_activated:
            message = {"message": "Your account has already been activated."}
            return Response(message, status=status.HTTP_200_OK)
        user.is_activated = True
        user.save()
        message = {"message": "Your account has been activated successfully"}
        return Response(message, status=status.HTTP_200_OK)


class ResetPasswordAPIView(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UserSerializer


    def post(self, request):
        serializer = self.serializer_class(request.user)
        email = request.data.get('email', None)
        if not email:
            message = {"message": "Please provide an email address"}
            return Response(message, status=status.HTTP_200_OK)
        user = serializer.get_user(email=email)
        token = user.token
        serializer.reset_password(email, token, request)
        message = {"message": "An email has been sent to your account"}
        return Response(message, status=status.HTTP_200_OK)


class UpdateUserAPIView(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UserSerializer


    def put(self, request, token):
        user = auth.authenticate_credentials(request, token)
        password = request.data.get('password', None)
        if not password:
            message = {"message": "Please provide a password"}
            return Response(message, status=status.HTTP_200_OK)
        if check_password(password, user.password):
            message = {"message": "Your new password can't be the same as the old password"}
            return Response(message, status=status.HTTP_200_OK)
        user.set_password(password)
        user.save()
        message = {"message": "Your password has been updated successfully"}
        return Response(message, status=status.HTTP_200_OK)
