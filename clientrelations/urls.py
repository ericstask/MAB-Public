from django.urls import path, reverse_lazy
from django.views.generic import RedirectView
from . import views

app_name = 'clientrelations'

urlpatterns = [
    path('general_tools', views.general_tools, name='general_tools'),
    path('other_tools', views.other_tools, name='other_tools'),
    path('aclient_tools', views.aclient_tools, name='aclient_tools'),

    path('tool_output', views.tool_output, name='tool_output'),

    path('aclient_call_log', views.aclient_call_log, name='aclient_call_log'),
    path('aclient_file_merger', views.aclient_file_merger, name='aclient_file_merger'),

    path('sectional_call_logs', views.sectional_call_logs, name='sectional_call_logs'),
    path('revo_weekly_invoice', views.revo_weekly_invoice, name='revo_weekly_invoice'),
    path('', RedirectView.as_view(url=reverse_lazy('other_tools'), permanent=True)),

    path('email_retrieval', views.email_retrieval, name='email_retrieval'),
    path('email_retrieval/search', views.email_search, name='email_search'),
    path('email_retrieval/search_status/<str:taskId>/', views.email_search_status, name='email_search_status'),
    path('email_retrieval/html/<str:emailID>/', views.email_retrieval_html, name='email_retrieval_html'),
    path('email_retrieval/eml/<str:emailID>/', views.email_retrieval_eml, name='email_retrieval_eml'),

    path('email_retrieval/bulk/', views.email_bulk_retrieval, name='email_bulk_retrieval'),
    path('email_retrieval/start_email_zip_task/', views.start_email_zip_task, name='start_email_zip'),
    path('email_retrieval/email_zip_status/<str:taskId>/', views.check_zip_task_status, name='email_zip_status'),
]