from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'operations'

urlpatterns = [
    path('reports', views.reports, name='reports'),

    path('reports/agent_productivity', views.agent_productivity, name='agent_productivity'),
    path('reports/agent_productivity/get_table_data', views.agent_productivity_get_table_data, name='agent_productivity_get_table_data'),
    path('reports/agent_productivity/create_excel_file', views.agent_productivity_create_excel_file, name='agent_productivity_create_excel_file'),
    path('reports/agent_productivity/create_pdf_file', views.agent_productivity_create_pdf_file, name='agent_productivity_create_pdf_file'),

    path('reports/collector_goal_summary', views.collector_goal_summary, name='collector_goal_summary'),
    path('reports/collector_goal_summary/get_table_data', views.collector_goal_summary_get_table_data, name='collector_goal_summary_get_table_data'),

    path('reports/pay_for_performance', views.pay_for_performance, name='pay_for_performance'),
    path('reports/pay_for_performance/add_remove', views.pay_for_performance_add_remove, name='pay_for_performance_add_remove'),
    path('reports/pay_for_performance/delete/<str:employee_id>', views.pay_for_performance_delete, name='pay_for_performance_delete'),
    path('reports/pay_for_performance/get_table_data', views.pay_for_performance_get_table_data, name='pay_for_performance_get_table_data'),

    path('tools', views.tools, name='tools'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
