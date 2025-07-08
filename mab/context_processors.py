from .models import UserDashboard


def dashboard_tools(request):
    if request.user.is_authenticated:
        links_in_dashboard = UserDashboard.objects.filter(user=request.user).select_related('link').order_by('link__name')
        link_names = [obj.link.name for obj in links_in_dashboard]
    else:
        link_names = []

    return {'links_in_dashboard': link_names}


def referring_url(request):
    return {'referring_url': request.META.get('HTTP_REFERER')}
