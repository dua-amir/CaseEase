from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class Case(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('In Progress', 'In Progress'),
        ('Waiting for Info', 'Waiting for Info'),
        ('Resolved', 'Resolved'),
        ('Closed', 'Closed'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending')
    location = models.CharField(max_length=200, null=True, blank=True)
    incident_date = models.DateField(null=True, blank=True)
    uploaded_file = models.FileField(upload_to='case_files/', null=True, blank=True)
    is_anonymous = models.BooleanField(default=False)
    suspect_name = models.CharField(max_length=200, null=True, blank=True)
    witnesses = models.TextField(null=True, blank=True)
    progress_notes = models.TextField(null=True, blank=True)
    report_file = models.FileField(upload_to='reports/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='cases_created'
    )
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='cases_assigned',
        limit_choices_to={'groups__name': 'handler'}
    )

    def __str__(self):
        return f"{self.title} ({self.status})"



class CaseHistory(models.Model):
    case = models.ForeignKey(Case, related_name='history', on_delete=models.CASCADE)
    action = models.CharField(max_length=255)
    performed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.action} on {self.timestamp}"
