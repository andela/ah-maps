"""The highlight text in article urls."""

from django.urls import path
from .views import AddHighlightAPIView

urlpatterns = [
    path('add/<slug>/', AddHighlightAPIView.as_view(), name='create_highlight'),
    path('remove/<article_slug>/<highlight_slug>/', AddHighlightAPIView.as_view(), name='remove_highlight'),
]
