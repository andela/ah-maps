from rest_framework.generics import (
  CreateAPIView,
  ListAPIView,
  ListCreateAPIView
)
from rest_framework.permissions import (
 IsAuthenticatedOrReadOnly,
 IsAdminUser
)

from django.apps import apps
from rest_framework.exceptions import NotFound, ValidationError
from django.core.mail import send_mail
from .serializers import ReportSerializer
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import get_template
from django.conf import settings
from rest_framework.response import Response
from rest_framework import serializers, status
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from .serializers import (
    TABLE, ReportSerializer
)

Article = apps.get_model('article', 'Article')

def get_article(slug):
    """
    This returns articles based on the slug
    """
    article = Article.objects.filter(slug=slug).first()
    if not article:
        message = {'message': 'Sorry, we have no article with that slug'}
        return message
    return article

def send_report_email(article, request):
        protocol = 'https://' if request.is_secure() else 'http://'
        current_site = get_current_site(request)
        article_link = protocol + current_site.domain + "/api/article/detail/" + article.slug + "/"
        data = {
                    'report_category' : request.data.get('category'),
                    'report_message': request.data.get('message'),
                    'report_username': request.user.username,
                    'article_link': article_link
                }
        html_content = render_to_string('report_email.html', data)
        text_content = strip_tags(html_content)
        from_email = settings.COMPANY_EMAIL
        admin_email = settings.ADMIN_EMAIL
        msg = EmailMultiAlternatives("Authors' Haven Reported Article" , text_content, from_email, (admin_email,))
        msg.attach_alternative(html_content, "text/html")
        msg.send()

        return True

class ReportAPIView(ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = ReportSerializer
    queryset = TABLE.objects.all()

    def post(self, request, slug):
        report = request.data
        article = get_article(slug)
        
        # ensures that article exists
        if isinstance(article, dict):
            raise ValidationError(detail={'article': 'Sorry, none of our articles has that slug'})

        # ensures a user cannot report his/her own article
        if article.user == request.user:
            raise ValidationError(detail={'author': 'Sorry, you cannot report your own article'})
        report.update({
            "user":request.user.id,
            "username":request.user.username,
            "article":article.id
            })
        serializer = self.serializer_class(data=report)
        serializer.is_valid(raise_exception=True)
        send_report_email(article, request)
        serializer.save()
        message = { "success" : "Your report has been successfully received"}
        return Response(message, status=status.HTTP_201_CREATED)
