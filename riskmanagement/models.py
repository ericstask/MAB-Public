from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class RiskManagementPermissions(models.Model):
    """
    Dummy model for defining custom permission related to Client Relations.
    """

    class Meta:
        managed = False  # don't create the model in the database
        permissions = [
            ("access_risk_management", "Can access the Risk Management section"),
        ]


class AuditType(models.Model):
    AUDIT_TYPE_DEPARTMENT_CHOICES = [
        ('posting', 'Posting'),
        ('performance', 'Performance'),
        ('information technology', 'Information Technology '),
        ('human resources', 'Human Resources'),
        ('compliance', 'Compliance'),
        ('collections', 'Collections'),
        ('accounting', 'Accounting'),
    ]

    AUDIT_TYPE_FREQUENCY_CHOICES = [
        (1, 'Daily'),  # key cooresponds to frequency of audits
        (7, 'Weekly'),
        (14, 'Bi-Weekly'),
        (30, 'Monthly'),
        (60, 'Bi-Monthly'),
        (90, 'Quartlery'),
        (180, 'Bi-Annually'),
        (356, 'Annually'),
    ]

    AUDIT_TYPE_RISK_LEVEL_CHOICES = [
        (2, 'High'),  # key cooresponds to the number of days a response is need in
        (3, 'Medium'),
        (5, 'Low'),
    ]
    
    department = models.CharField(choices=AUDIT_TYPE_DEPARTMENT_CHOICES)  # area of business the audit is focused on 
    name = models.CharField(max_length=255)  # name of the audit
    risk_level = models.IntegerField(choices=AUDIT_TYPE_RISK_LEVEL_CHOICES)  # the level of impact issues have on the company and clients
    testing_frequency = models.IntegerField(choices=AUDIT_TYPE_FREQUENCY_CHOICES)  # how often the audit is performed
    passing_score = models.IntegerField()  # not sure if this is actually needed

    def __str__(self):
        return self.name


class Audit(models.Model):
    AUDIT_CLIENT_CHOICES = [
        (0, 'Business'),  
        (1, "Collections"),
        (2, 'REM'),  
        (3, 'AnotherBank'),
        (4, 'AClient'),
        (5, 'InsuranceComp'),
        (6, 'Bank'),
        (7, 'AStore'),
        (8, 'Finance'),
        (9, 'Clothes'),
        (10, 'The Bank'),
    ]

    audit_type = models.ForeignKey(AuditType, on_delete=models.CASCADE)  # the audit that was conducted
    auditor = models.ForeignKey(User, on_delete=models.CASCADE, null=True)  # the person performing the audit
    client = models.IntegerField(choices=AUDIT_CLIENT_CHOICES, default=0)  # client associated with the audit
    start_date = models.DateField()  # date when audit becomes available to run
    due_date = models.DateField()  # the date the audit needs to be done by
    date_ran = models.DateField(null=True)  # date the audit was run
    created_at = models.DateTimeField(auto_now_add=True)  # date audit was created
    eval_start_date = models.DateField(null=True)  # the begining of the period that was aduited
    eval_end_date =  models.DateField(null=True)  # the end of the period audited 

    def next_audit_date(self):
        return self.due_date + timezone.timedelta(days=self.audit_type.testing_frequency)


class AuditFinding(models.Model):
    AUDIT_STATUS_CHOICES = [
        (1, 'Open'),
        (2, 'Closed'),
        (3, 'In Progress'),
    ]

    audit = models.ForeignKey(Audit, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    date_identified = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=AUDIT_STATUS_CHOICES)
    assigned_to = models.ForeignKey(User, on_delete=models.PROTECT)
    description = models.TextField()
    recommendations = models.TextField()
    actions_taken = models.TextField()
    documentation = models.FileField(upload_to='audit_documents', null=True, blank=True)  # Need to actually set up a location to store these

    def remediation_due_date(self):
        return self.date_identified + timezone.timedelta(days=self.audit.audit_type.risk_level)


class StateDialingAudit(models.Model):
    audit = models.OneToOneField(Audit, on_delete=models.CASCADE)
    calls_evaluated = models.IntegerField(null=True)  
    unique_calls_evaluated = models.IntegerField(null=True)
    fdcpa_early	= models.IntegerField(null=True)
    fdcpa_Late = models.IntegerField(null=True)
    michigan_early = models.IntegerField(null=True)	
    oklahoma_early = models.IntegerField(null=True)	
    oregon_early = models.IntegerField(null=True)
    texas_early	= models.IntegerField(null=True)
    texas_sunday = models.IntegerField(null=True)

    def total_defective(self):
        total = self.fdcpa_early + self.fdcpa_Late + self.michigan_early + self.oklahoma_early + self.oregon_early + self.texas_early + self.texas_sunday
        return(total)


class CallsPerWeekAudit(models.Model):
    audit = models.OneToOneField(Audit, on_delete=models.CASCADE)
    calls_evaluated = models.IntegerField(null=True)  
    unique_calls_evaluated = models.IntegerField(null=True) 


class CallsPerWeekExtraCalls:
    calls_per_week_audit = models.OneToOneField(CallsPerWeekAudit, on_delete=models.CASCADE)  # audit it is associated with
    cubs_account_number = models.IntegerField()  # the account that was called
    num_of_calls = models.IntegerField()  # number of calls made in time period


class CallsPerWeekReview(models.Model):
    calls_per_week_audit = models.OneToOneField(CallsPerWeekAudit, on_delete=models.CASCADE)  # audit it is associated with
    cubs_account_number = models.IntegerField()	# the account that was called
    call_date = models.DateTimeField()  # the begining of the time period where contatct was made
    end_date = models.DateTimeField()  # the date it would have been okay to call again
    contact_tally = models.IntegerField()  # number of calls made in that period
    notes = models.TextField(null=True)  # evidence that the call was okay or not okay
