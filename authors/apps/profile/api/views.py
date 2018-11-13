"""Define the profile views."""

from rest_framework import status
from rest_framework.generics import (
    ListAPIView,
    RetrieveUpdateAPIView,
    RetrieveAPIView,
    RetrieveUpdateDestroyAPIView,
)

from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly,
    IsAuthenticated
)

from rest_framework.response import Response
from .serializers import (
    TABLE, ProfileListSerializer, ProfileUpdateSerializer, User, ProfileFollowSerializer
)

from ...core.permissions import IsOwnerOrReadOnly


def get_profile(username):
    """Get user profile from their username."""
    try:
        profile = TABLE.objects.get(user__username=username)
    except TABLE.DoesNotExist:
        raise serializers.ValidationError(
            'User {} does not exist.'.format(username))
    return profile


class ProfileListAPIView(ListAPIView):
    """List profiles view."""

    permission_classes = [IsAuthenticated]
    serializer_class = ProfileListSerializer
    queryset = TABLE.objects.all()


class ProfileDetailAPIView(RetrieveAPIView):
    """Get profile details View."""

    queryset = TABLE.objects.all()
    serializer_class = ProfileListSerializer
    lookup_field = 'user__username'


class MyProfileDetailAPIView(RetrieveAPIView):
    """Get current user profile view."""

    permission_classes = (IsAuthenticated,)
    serializer_class = ProfileListSerializer

    def get(self, request, *args, **kwargs):
        """List Profiles."""
        # There is nothing to validate or save here. Instead, we just want the
        # serializer to handle turning our `User` object into something that
        # can be JSONified and sent to the client.
        serializer = self.serializer_class(request.user.profile)

        return Response(serializer.data, status=status.HTTP_200_OK)


class ProfileUpdateAPIView(RetrieveUpdateAPIView):
    """Update a user profile."""

    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    queryset = TABLE.objects.all()
    serializer_class = ProfileUpdateSerializer
    lookup_field = 'user__username'


class FollowProfilesAPIView(RetrieveUpdateDestroyAPIView):
    """Follow and Unfollow a profile endpoint."""

    permission_classes = (IsAuthenticated,)
    serializer_class = ProfileFollowSerializer

    def post(self, request, username):
        """Follow a user."""
        serializer = self.serializer_class(
            data={"username": username}, context={'request': request})
        serializer.is_valid(username)
        serializer.save()
        message = {"success": "User {} followed successfully".format(username)}
        return Response(message, status=status.HTTP_200_OK)

    def delete(self, request, username):
        """Unfollow a user."""
        # check if user exists
        serializer = self.serializer_class(data={"username": username})
        serializer.is_valid()
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            message = {"error": "User {} does not exists".format(username)}
            return Response(message, status=status.HTTP_404_NOT_FOUND)

        # check if you are following that user
        current_profile = request.user.profile
        user = current_profile.is_following.filter(user__username__exact=username).values_list('user__username')
        if not user:
            message = {
                "error": "You cannot unfollow someone that you don't follow"}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)

        # unfollow that user
        profile = get_profile(username)
        current_profile.unfollow(profile=profile)
        message = {
            "success": "User {} unfollowed successfully".format(username)}
        return Response(message, status=status.HTTP_200_OK)


class ListFollowingProfilesAPIView(RetrieveAPIView):
    """List profiles a user is following."""

    permission_classes = (IsAuthenticated,)
    serializer_class = ProfileFollowSerializer

    def get(self, request, username):
        """Get following."""
        serializer = self.serializer_class(data={"username": username})
        serializer.is_valid(username)
        profile = get_profile(username)
        following = profile.following(profile=profile).values('user__username', 'image')
        message = {"following": following}
        return Response(message, status=status.HTTP_200_OK)


class ListFollowersProfilesAPIView(RetrieveAPIView):
    """List profiles a user is being followed by."""

    permission_classes = (IsAuthenticated,)
    serializer_class = ProfileFollowSerializer

    def get(self, request, username):
<<<<<<< HEAD
        """Get followers."""
=======
        """get followers"""
>>>>>>> feat(bookmarks): Bookmark articles for reading later
        serializer = self.serializer_class(data={"username": username})
        serializer.is_valid(username)
        profile = get_profile(username)
        followers = profile.get_followers(profile=profile).values('user__username', 'image')
        message = {"followers": followers}
        return Response(message, status=status.HTTP_200_OK)
