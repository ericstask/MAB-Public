from django.contrib import admin
from .models import DashboardLink
from riskmanagement.models import AuditType

@admin.register(DashboardLink)
class DashboardLinkAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'link', 'department', 'type',)
    search_fields = ('name',)


@admin.register(AuditType)
class AuditTypeAdmin(admin.ModelAdmin):
    list_display = ('department', 'name', 'risk_level', 'testing_frequency', 'passing_score',)
    search_fields = ('department', 'name', 'risk_level', 'testing_frequency',)    
    