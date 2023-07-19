from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import permissions

from pages.models import Note
from pages.serializers import NoteSerializer

# Create your views here.

class NoteViewSet(viewsets.ModelViewSet):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = [permissions.AllowAny]
