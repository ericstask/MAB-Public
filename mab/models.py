from django.db import models
from django.contrib.auth.models import User

class DashboardLink(models.Model):
    DEPARTMENT_CHOICES = [
        (1, 'Client Relations'),
        (2, 'Collections'),
        (3, 'Customer Service'),
        (4, 'Human Resources'),
        (5, 'Information Technology'),
        (6, 'Operations'),
        (7, 'Postng'),
        (8, 'Quality Assurance'),
        (9, 'Training'),
        (10, 'Risk Management'),
    ]

    TOOL_TYPE_CHOICES = [
        (1, 'Tool'),
        (2, 'Report'),
    ]

    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    link = models.CharField(max_length=255)
    department = models.IntegerField(choices=DEPARTMENT_CHOICES)
    type = models.IntegerField(choices=TOOL_TYPE_CHOICES)

    def get_department_disply(self):
        return dict(self.DEPARTMENT_CHOICES).get(self.department, '')
    
    def get_type_display(self):
        return dict(self.TOOL_TYPE_CHOICES).get(self.type, '')


class UserDashboard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    link = models.ForeignKey(DashboardLink, on_delete=models.CASCADE)

class Notifications(models.Model):
    NOTIFICATION_PRIORITY_CHOICES = [
        (1, 'High'),
        (2, 'Medium'),
        (3, 'Low'),
    ]

    NOTIFICATION_ACTION_CHOICES = [
        (1, 'View'),  # simply view notification
        (2, 'Reply'),  # request reply
        (3, 'Notify'),  # notify when read
        (4, 'Review'),  # accept or reject
    ]

    recipient = models.ForeignKey(User, related_name='received_notifications', on_delete=models.CASCADE)
    sender = models.ForeignKey(User, related_name='sent_notifications', on_delete=models.CASCADE, null=True, blank=True)
    action = models.IntegerField(choices=NOTIFICATION_ACTION_CHOICES)
    priority = models.IntegerField(choices=NOTIFICATION_PRIORITY_CHOICES)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_seen = models.BooleanField(default=False)
    is_read = models.BooleanField(default=False)
    link = models.CharField(max_length=255)

