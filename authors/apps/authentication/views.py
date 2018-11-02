from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView, CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from social_django.utils import load_backend, load_strategy
from social_core.backends.oauth import BaseOAuth1, BaseOAuth2
from social_core.exceptions import MissingBackend

from .renderers import UserJSONRenderer
from .serializers import (
    LoginSerializer, RegistrationSerializer, UserSerializer,SocialSignUpSerializer
)


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
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


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


class SocialSignUp(CreateAPIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = SocialSignUpSerializer

    def create(self, request, *args, **kwargs):
        """ Function to interrupt social_auth authentication pipeline"""
        #pass the request to serializer to make it a python object
        #serializer also catches errors of blank request objects
        serializer = self.serializer_class(data=request.data) 
        serializer.is_valid(raise_exception=True)

        provider = serializer.data.get('provider', None)
        strategy = load_strategy(request) #creates the app instance

        if request.user.is_anonymous: #make sure the user is not anonymous
            user=None
        else:
            user=request.user
    

        try:
            #load backend with strategy and provider from settings(AUTHENTICATION_BACKENDS)
            backend = load_backend(strategy=strategy, name=provider, redirect_uri=None)
        
        except MissingBackend as error:
            
            return Response({
                "errors": str(error)
            }, status=status.HTTP_400_BAD_REQUEST)
            
        try:
            #check type of oauth provide e.g facebook is BaseOAuth2 twitter is BaseOAuth1
            if isinstance(backend, BaseOAuth1):
                #oath1 passes access token and secret
                access_token = {
                        "oauth_token": serializer.data.get('access_token'),
                        "oauth_token_secret": serializer.data.get('access_token_secret'),
                        }

            elif isinstance(backend, BaseOAuth2):
                #oauth2 only has access token
                access_token = serializer.data.get('access_token')

        except HTTPError as e:
            return Response({
                "error": {
                    "access_token": "invalid token",
                    "details": str(e)
                }
            }, status=status.HTTP_400_BAD_REQUEST)


        #authenticate the user(signup/login) with the user instance and the access_token received
        authenticated_user = backend.do_auth(access_token, user=user)

        if authenticated_user and authenticated_user.is_active:
            #Check if the user you intend to authenticate is active
            
            headers = self.get_success_headers(serializer.data)
            response = {"email":authenticated_user.email,
                        "username":authenticated_user.username,
                        "token":authenticated_user.token} 
                       
            return Response(response,status=status.HTTP_201_CREATED,
                                headers=headers)
        else:
            return Response({"errors": "Could not authenticate"},
                            status=status.HTTP_400_BAD_REQUEST)
