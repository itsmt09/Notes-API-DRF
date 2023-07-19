from django.db import models

class Note(models.Model):

    ARC = 'ARCHIVED'
    DRA = 'DRAFT'
    PUB = 'PUBLISHED'

    status_choices = [
        (ARC, 'Archived'),
        (DRA, 'Draft'),
        (PUB, 'Published')
    ]
    title = models.CharField(max_length=100, blank=True, default='')
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices = status_choices, max_length = 10, default=DRA)

    def __str__(self):
        return str(self.title)
    
    class Meta:
        ordering = ['-created']
