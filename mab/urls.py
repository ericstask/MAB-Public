"""
URL configuration for mab project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import include, path, reverse_lazy
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('add_tool/<str:link_name>', views.add_tool_to_dashboard, name='add_tool_to_dashboard'),
    path('remove_tool/<str:link_name>', views.remove_tool_from_dashboard, name='remove_tool_from_dashboard'),
    path('admin', admin.site.urls),
    path('clientrelations/', include('clientrelations.urls', namespace='clientrelations')),
    path('operations/', include('operations.urls', namespace='operations')),
    path('riskmanagement/', include('riskmanagement.urls', namespace='riskmanagement')),
    path('', RedirectView.as_view(url=reverse_lazy('login'), permanent=True)),
]
