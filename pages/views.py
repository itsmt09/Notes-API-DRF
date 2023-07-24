from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import permissions

from pages.models import Note
from pages.serializers import NoteSerializer
from django_filters import rest_framework as filters


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
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = NoteFilter
    # filterset_fields = ['status']

    # def get_queryset(self):
    #     queryset = Note.objects.all()
    #     query_status = self.request.query_params.get('status')
    #     if query_status is not None:
    #         queryset = queryset.filter(status = query_status.upper())
    #     return queryset