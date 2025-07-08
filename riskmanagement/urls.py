from django.urls import path
from . import views

app_name = 'riskmanagement'

urlpatterns = [
    path('overview', views.overview, name='overview'),
    path('create_audit', views.create_or_edit_audit, name='create_audit'),
    path('edit_audit/<int:audit_id>', views.create_or_edit_audit, name='edit_audit'),
    path('delete_audit/<int:audit_id>', views.delete_audit, name='delete_audit'),

    path('calls_per_week', views.calls_per_week_audit, name='calls_per_week_audit'),
    path('state_dialing', views.state_dialing_audit, name='calls_per_week_audit'),

    path('api/audits', views.audit_list_view.as_view(), name='audit-list'),
]
