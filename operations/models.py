from django.db import models
import os


class OperationsPermissions(models.Model):
    """
    Dummy model for defining custom permission related to Client Relations.
    """

    class Meta:
        managed = False  # don't create the model in the database
        permissions = [
            ("access_operations", "Can access the Operations section"),
        ]
        


# Create your models here.
class PayForPerformance(models.Model):
    file_title = models.CharField(max_length=255)
    uploaded_file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def delete(self, *args, **kwargs):
        if self.uploaded_file:
            if os.path.isfile(self.uploaded_file.path):
                os.remove(self.uploaded_file.path)
        super(PayForPerformance, self).delete(*args, **kwargs)

    def __str__(self):
        return self.file_title


class PayForPerformanceEmployee(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    last_name_and_suffix = models.CharField()
    first_name = models.CharField()
    most_recent_hire_date = models.DateField(null=True, blank=True)
    supervisor = models.CharField(null=True, blank=True)
    pay_rate = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=20, choices=[('added', 'Added'), ('removed', 'Removed')])
    is_removed = models.BooleanField(default=False)


class AgentProductivity(models.Model):
    productvity_file_title = models.CharField(max_length=255)
    productivity_uploaded_file = models.FileField(upload_to='uploads/')
    calls_file_title = models.CharField(max_length=255)
    calls_uploaded_file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def delete(self, *args, **kwargs):
        if self.productivity_uploaded_file:
            if os.path.isfile(self.productivity_uploaded_file.path):
                os.remove(self.productivity_uploaded_file.path)
        if self.calls_uploaded_file:
            if os.path.isfile(self.calls_uploaded_file.path):
                os.remove(self.calls_uploaded_file.path)
        super(AgentProductivity, self).delete(*args, **kwargs)
