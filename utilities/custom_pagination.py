from rest_framework.pagination import PageNumberPagination
from pages.models import Note

class CustomPageNumberPagination(PageNumberPagination):
    page_size_query_param = 'page_size'
    max_page_size = Note.objects.count()