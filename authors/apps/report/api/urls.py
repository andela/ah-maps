from django.urls import path
from .views import (
   ReportAPIView
)

from ...article.api.views import ReportedArticleListAPIView

urlpatterns = [
    path('<slug>', ReportAPIView.as_view(), name='report'),
    path('all/', ReportedArticleListAPIView.as_view(), name="list")
]
