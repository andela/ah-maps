from django.db import models
from django.utils.translation import pgettext_lazy as _
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from versatileimagefield.fields import VersatileImageField

User = get_user_model()


class ProfileManager(models.Manager):
    def create_profile(self, **kwargs):
        self.model.create(user=kwargs['instance'])


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        related_name='profile',
        on_delete=models.CASCADE,
        primary_key=True,
    )
    image = VersatileImageField(
        'Image',
        upload_to='profile/',
        width_field='width',
        height_field='height',
        blank=True,
        null=True
    )
    height = models.PositiveIntegerField(
        'Image Height',
        blank=True,
        null=True
    )
    width = models.PositiveIntegerField(
        'Image Width',
        blank=True,
        null=True
    )
    bio = models.TextField(
        _('Profile Field', 'bio'),
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(
        _('Profile field', 'created at'),
        auto_now_add=True,
        editable=False
    )
    updated_at = models.DateTimeField(
        _('Profile field', 'updated at'),
        auto_now=True
    )
    is_following = models.ManyToManyField('self', related_name='followers', symmetrical=False)


    class Meta:
        app_label = 'profile'


    def __str__(self):
        return self.user.username


    def follow(self, profile):
        self.is_following.add(profile)


    def unfollow(self, profile):
        self.is_following.remove(profile)


    def get_followers(self, profile=None):
        if profile:
            return profile.followers.all().values_list('user__username', flat=True)
        return self.followers.all().values_list('user__username', flat=True)


    def following(self, profile=None):
        if profile:
            return profile.is_following.all().values_list('user__username', flat=True)
        return self.is_following().all().values_list('user__username', flat=True)



def create_profile(sender, **kwargs):
    if kwargs['created']:
        Profile.objects.create(user=kwargs['instance'])


create_profile_signal = post_save.connect(create_profile, sender=get_user_model())
