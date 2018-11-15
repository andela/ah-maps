from django.db import models
from autoslug import AutoSlugField


class Tag(models.Model):
    """Tag model"""

    tag = models.CharField(max_length=28)	
    slug = AutoSlugField(populate_from='tag', blank=True, null=True, unique=True)

    class Meta:
        ordering = ['tag']

    def __str__(self):
        return self.tag