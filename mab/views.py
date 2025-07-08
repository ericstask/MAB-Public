from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import DashboardLink, UserDashboard

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect(reverse('dashboard'))
        else:
            return render(request, 'mab/login.html', {'error_message': 'Invalid credentials'})
    else:
        if request.user.is_authenticated:
            return redirect('dashboard')
        else:
            return render(request, 'mab/login.html')
    

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def dashboard(request):
    links_in_dashboard = UserDashboard.objects.filter(user=request.user).select_related('link').order_by('link__name')
    return render(request, 'mab/dashboard.html', {'links_in_dashboard': links_in_dashboard})


@login_required
def add_tool_to_dashboard(request, link_name):
    user = request.user
    link = DashboardLink.objects.get(name=link_name)

    if not UserDashboard.objects.filter(user=user, link=link).exists():
        UserDashboard.objects.create(user=user, link=link)
        messages.success(request, f"{link.name} has been added to your dashboard")

    referring_url = request.META.get('HTTP_REFERER')
    if referring_url:
        return redirect(referring_url)
    else:
        return redirect('dashboard')


@login_required
def remove_tool_from_dashboard(request, link_name):
    link = DashboardLink.objects.get(name=link_name)
    user_dashboard_entry = get_object_or_404(UserDashboard, user=request.user, link=link)

    user_dashboard_entry.delete()
    messages.success(request, f"{link.name} has been removed from your dashboard")

    referring_url = request.META.get('HTTP_REFERER')
    if referring_url:
        return redirect(referring_url)
    else:
        return redirect('dashboard')
