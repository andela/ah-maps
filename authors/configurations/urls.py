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
from django.contrib import admin

urlpatterns = [
    path('', include(('authors.apps.profile.urls', 'profile'), namespace='profile')),
    path('admin/', admin.site.urls),
    path('api/', include(('authors.apps.authentication.urls', 'authentication'), namespace='authentication')),
]
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', include(('authors.apps.profile.urls', 'profile'), namespace='profile')),
    path('api/article/', include(('authors.apps.article.api.urls', 'article_api'), namespace='article_api')),
    path('api/profile/', include(('authors.apps.profile.api.urls', 'profile_api'), namespace='profile_api')),
    path('admin/', admin.site.urls),
    path('api/', include(('authors.apps.authentication.urls', 'authentication'), namespace='authentication')),
    path('oauth/', include('social_django.urls',  namespace='social')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

