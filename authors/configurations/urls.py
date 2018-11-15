"""authors URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.urls import include, path
from django.conf.urls.static import static
from django.contrib import admin
from django.conf import settings

from rest_framework_swagger.views import get_swagger_view

swagger_view = get_swagger_view(title='ah-maps-API')

urlpatterns = [
    path('ahmaps/swagger/', swagger_view),
    path('', include(('authors.apps.profile.urls', 'profile'), namespace='profile')),
    path('api/article/', include(('authors.apps.article.api.urls',
                                  'article_api'), namespace='article_api')),
    path('api/tag/', include(('authors.apps.tags.api.urls',
                                  'tag_api'), namespace='tag_api')),
    path('api/favorite/', include(('authors.apps.favorite.api.urls',
                                   'favorite_api'), namespace='favorite_api')),
    path('api/profile/', include(('authors.apps.profile.api.urls',
                                  'profile_api'), namespace='profile_api')),
    path('api/rate/', include(('authors.apps.rating.api.urls',
                               'rate_api'), namespace='rating_api')),
    path('api/articles/comment/', include(('authors.apps.comment.api.urls', 'comment_api'), namespace='comment_api')),
    path('api/', include(('authors.apps.authentication.urls',
                          'authentication'), namespace='authentication')),
    path('oauth/', include('social_django.urls',  namespace='social')),
    path('api/bookmarks/', include(('authors.apps.bookmarks.api.urls',
                                    'bookmarks'), namespace='bookmark_api')),
    path('api/read/', include(('authors.apps.read_stats.api.urls',
                                    'read_stats'), namespace='read_stats_api')),
    path('api/highlights/', include(('authors.apps.highlights.api.urls',
                                    'highlights'), namespace='highlights_api')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
