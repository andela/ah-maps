from django.urls import path
from .views import (
   ArticleTagsAPIView,
   TagsView,	
)
	
urlpatterns = [	
    path('', TagsView.as_view(), name='list'),	
    path('<slug>', ArticleTagsAPIView.as_view(), name='create_tags'),	
]