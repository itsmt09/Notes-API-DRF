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
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = (filters.DjangoFilterBackend, SearchFilter,)
    filterset_class = NoteFilter
    search_fields = ['title', 'description',]

    def send_email(request):
        subject = "Django mail Check"
        message = "Django mail has been sent using Celery"
        receiver_email = "manish.tekam.9@gmail.com"
        send_email_check.delay(subject, message, settings.EMAIL_HOST_USER, receiver_email)
        return HttpResponse("Sent Email Successfully...Check your email please")


    # filterset_fields = ['status']

    # def get_queryset(self):
    #     queryset = Note.objects.all()
    #     query_status = self.request.query_params.get('status')
    #     if query_status is not None:
    #         queryset = queryset.filter(status = query_status.upper())
    #     return queryset