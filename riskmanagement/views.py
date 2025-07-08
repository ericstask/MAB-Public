from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.utils import timezone
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.db.models import Case, When, Value, CharField
from .models import Audit, StateDialingAudit, CallsPerWeekAudit
from .forms import AuditForm

from datetime import datetime
import subprocess
import json

from rest_framework import generics
from .serializers import AuditSerializer
# from mab.utils.pagination import CustomPagination


@login_required
@permission_required('riskmanagement.access_risk_management', raise_exception=True)
def overview(request):
    incomplete_aduits = Audit.objects.filter(date_ran__isnull=True).order_by('due_date')
    current_time = timezone.now().date()

    overview_context = {
        'audits': incomplete_aduits,
        'now': current_time,
    }

    return render(request, 'riskmanagement/riskmanagement_overview.html', overview_context)


@login_required
@permission_required('riskmanagement.access_risk_management', raise_exception=True)
def calls_per_week_audit(request):
    if request.method == 'POST':
        selected_audit_ids = request.POST.getlist('selected_audits')
        audits_to_run = Audit.objects.filter(id__in=selected_audit_ids, date_ran__isnull=True)
        
        print(selected_audit_ids)

        python_executable_path = "/mnt/python/python.exe"
        script_path = ""

        sql_query = "SELECT * FROM Employee"
        table = "Employee"

        result = subprocess.run([python_executable_path, script_path, sql_query, table], capture_output=True, text=True)

        if result.stderr:
            print(result.stderr)

        # data = json.loads(result.stdout)

        print(result.stdout)

        # return JsonResponse(data, safe=False)

    available_audits = Audit.objects.filter(audit_type__name='Calls Per Week', date_ran__isnull=True)

    return render(request, 'riskmanagement/calls_per_week.html', {'available_audits': available_audits})


@login_required
@permission_required('riskmanagement.access_risk_management', raise_exception=True)
def state_dialing_audit(request):
    return render(request, 'riskmanagement/state_dialing.html')


@login_required
@permission_required('riskmanagement.access_risk_management', raise_exception=True)
def create_or_edit_audit(request, audit_id=None):
    if audit_id:
        audit_instance = get_object_or_404(Audit, id=audit_id)
        audit_form = AuditForm(request.POST or None, instance=audit_instance)
        editing = True
    else:
        audit_instance = None
        audit_form = AuditForm(request.POST or None)
        editing = False

    if request.method == 'POST':
        
        if audit_form.is_valid():
            audit_instance = audit_form.save()

            submitted_audit_type = audit_instance.audit_type.name

            if str(submitted_audit_type) == 'State Dialing':
                specific_aduit, created = StateDialingAudit.objects.get_or_create(audit=audit_instance)
            elif str(submitted_audit_type) == 'Calls Per Week':
                specific_aduit, created = CallsPerWeekAudit.objects.get_or_create(audit=audit_instance)
            else:
                # SOMETHING BROKE!
                return HttpResponse("Invalid audit type")
            specific_aduit.save()

            messages.success(request, f'{str(submitted_audit_type)} Audit was successfully created.')
            return redirect('riskmanagement:overview')
            
    create_or_edit_context = {
        'audit_form': audit_form,
        'editing': editing,
    }
    return render(request, 'riskmanagement/create_or_edit_audit.html', create_or_edit_context)


@login_required
@permission_required('riskmanagement.access_risk_management', raise_exception=True)
def delete_audit(request, audit_id):
    audit = get_object_or_404(Audit, pk=audit_id)
    audit.delete()

    messages.success(request, f'{audit.audit_type.name}  Audit was successfully deleted.')
    return redirect('riskmanagement:overview')


class audit_list_view(generics.ListAPIView):
    today = datetime.today()

    queryset = Audit.objects.annotate(
        position=Case(
            When(due_date__lt=today, then=Value('0')),
            When(start_date__gt=today, then=Value('2')),
            default=Value('1'),
            output_field=CharField(),
        )
    )
    queryset = queryset.filter(date_ran__isnull=True).order_by('position')


    # queryset = Audit.objects.filter(date_ran__isnull=True).order_by('start_date', 'due_date')
    serializer_class = AuditSerializer
    # pagination_class = CustomPagination
    