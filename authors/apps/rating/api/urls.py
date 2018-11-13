from django.urls import path
from .views import (
   RateAPIView
)

urlpatterns = [
    path('<slug>/', RateAPIView.as_view(), name='rate')
]
