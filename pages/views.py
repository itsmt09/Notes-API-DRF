from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import permissions

from pages.models import Note
from pages.serializers import NoteSerializer
from django_filters import rest_framework as filters
from rest_framework.filters import SearchFilter
from pages.task import send_email_check
from notes import settings
from django.core.cache import cache
import redis

from rest_framework.response import Response

redis_instance = redis.StrictRedis(host='127.0.0.1', port=6379, db=1)

# filterset classes
class NoteFilter(filters.FilterSet):
    status = filters.CharFilter(field_name='status', lookup_expr='iexact')
    title = filters.CharFilter(field_name='title', lookup_expr='icontains')

    class Meta:
        model = Note
        fields = ['status', 'title']

# Create your views here.

class NoteViewSet(viewsets.ModelViewSet):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = (filters.DjangoFilterBackend, SearchFilter,)
    filterset_class = NoteFilter
    search_fields = ['title', 'description',]

    def send_email(request):
        subject = "Django mail Check"
        message = "Django mail has been sent using Celery"
        receiver_email = "manish.tekam.9@gmail.com"
        send_email_check.delay(subject, message, settings.EMAIL_HOST_USER, receiver_email)
        return HttpResponse("Sent Email Successfully...Check your email please")
    
    def list(self, request):
        title = self.request.query_params.get('title')

        if title is not None:
            cache_key = 'title' + title
        else:
            cache_key = 'title'

        if cache_key in cache:
            print("redis")
            queryset = cache.get(cache_key)
            return Response(queryset)
        else:
            print("db")
            queryset = Note.objects.all()
            if title is not None:
                queryset = queryset.filter(title__contains = title)

            serializer_class = NoteSerializer(queryset, many=True)
            cache.set(cache_key, serializer_class.data, timeout=60*60*2)
            return Response(serializer_class.data) 


    # filterset_fields = ['status']

    # def get_queryset(self):
    #     queryset = Note.objects.all()
    #     query_status = self.request.query_params.get('status')
    #     if query_status is not None:
    #         queryset = queryset.filter(status = query_status.upper())
    #     return queryset