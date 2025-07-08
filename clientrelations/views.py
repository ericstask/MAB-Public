import os
import json
import requests
import zipfile
import pandas as pd
from datetime import datetime, timedelta
from urllib.parse import urlencode
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.core import serializers
from django.core.cache import cache
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.generator import BytesGenerator
from io import BytesIO
from mab.utils.file_utils import retreive_header_and_footer
from mab.utils.email_utils import send_email_with_attachment
from mab.utils.archiving_utils import safe_move
from mab.utils.clientrelations_excel_report_utils import create_bank_sif_report, create_revo_weekly_invoices, create_aclient_call_logs, create_sectional_call_logs
from mab.tasks import fetch_letter_data, build_email_zip_for_client
from celery.result import AsyncResult

# Views that just display pages
@login_required
@permission_required('clientrelations.access_client_relations', raise_exception=True)
def general_tools(request):
    return render(request, 'clientrelations/general_tools.html')


@login_required
@permission_required('clientrelations.access_client_relations', raise_exception=True)
def other_tools(request):
    return render(request, 'clientrelations/other_tools.html')


@login_required
@permission_required('clientrelations.access_client_relations', raise_exception=True)
def aclient_tools(request):
    return render(request, 'clientrelations/aclient_tools.html')


# View used to output information after a client relations tools has been used
@login_required
@permission_required('clientrelations.access_client_relations', raise_exception=True)
def tool_output(request):
    return render(request, 'clientrelations/tool_output.html')


# Views with unique functions #######################################################################
@login_required
@permission_required('clientrelations.access_client_relations', raise_exception=True)
def email_retrieval(request):
    return render(request, 'clientrelations/cr_tool_templates/email_retrieval.html')


@login_required
@permission_required('clientrelations.access_client_relations', raise_exception=True)
def email_search(request):
    if request.method == "POST":
        letter_search_post_data = json.loads(request.body)
        # Trigger celery task
        task = fetch_letter_data.delay(letter_search_post_data)
        # Return the task id so the front-end can poll for results
        return JsonResponse({'task_id': task.id}, safe=False)
    

@login_required
def email_search_status(request, taskId):
    result = AsyncResult(taskId)
    if result.ready():
        # When task is complete, return the result
        return JsonResponse(result.result, safe=False)
    else:
        return JsonResponse({'status': 'PENDING'})


def email_retrieval_html(request, emailID):
    api_url = f'http://host.docker.internal:3000/api/letters?ReceivedEmailID={emailID}'

    try:
        response = requests.get(api_url, headers={ 'x-api-key': os.getenv('API_KEY') })
        response.raise_for_status()

        letter_data = response.json()['results']

    except requests.exceptions.RequestException as e:
        print(e)
        pass
        # TODO: THIS PROBABLY WON"T WORK HERE
        #messages.error(request, f"An error occured using the KPI API: {str(e)}.")


    return HttpResponse(letter_data[0]['HTML'])


def email_retrieval_eml(request, emailID):
    api_url = f'http://host.docker.internal:3000/api/letters?ReceivedEmailID={emailID}'

    try:
        response = requests.get(api_url, headers={ 'x-api-key': os.getenv('API_KEY') })
        response.raise_for_status()

        letter_data = response.json()['results']

    except requests.exceptions.RequestException as e:
        print(e)
        pass
        # TODO: THIS PROBABLY WON"T WORK HERE
        #messages.error(request, f"An error occured using the KPI API: {str(e)}.")

    email_datetime_obj = datetime.strptime(letter_data[0]['EmailDate'], "%Y-%m-%dT%H:%M:%S.000Z")
    formated_email_date = email_datetime_obj.strftime("%a, %d %b %Y %H:%M:%S +0000")

    email = MIMEMultipart()
    email['Subject'] = letter_data[0]['EmailSubject']
    email['From'] = letter_data[0]['EmailFrom']
    email['To'] = letter_data[0]['EmailTo']
    email['Date'] = formated_email_date

    body = letter_data[0]['HTML']
    email.attach(MIMEText(body, "html"))

    email_content = email.as_string()

    response = HttpResponse(
        email_content,
        content_type="message/rfc822",
    )
    filename = letter_data[0]['ReferenceNumber']
    response["Content-Disposition"] = f"attachment; filename={filename}.eml"
    return response


# Email Bulk Download Views
@login_required
@permission_required('clientrelations.access_client_relations', raise_exception=True)
def email_bulk_retrieval(request):
    return render(request, 'clientrelations/cr_tool_templates/email_zip_retrieval.html')


@login_required
@permission_required('clientrelations.access_client_relations', raise_exception=True)
def start_email_zip_task(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=400)
    
    data = json.loads(request.body)
    client = data.get('client')
    date = data.get('email_date')

    if not client or not date:
        return JsonResponse({'error': 'Missing client or date'}, status=400)
    
    task = build_email_zip_for_client.delay(client, date)
    return JsonResponse({'task_id': task.id})


@login_required
def check_zip_task_status(request, taskId):
    result = AsyncResult(taskId)

    if result.ready():
        if result.successful():
            return JsonResponse(result.result)
        else:
            return JsonResponse({'status': 'error', 'message': 'Task Failed'}, status=500)
    else:
        return JsonResponse({'status': 'pending'})
    

@login_required
def download_email_zip(request, token):
    zip_data = cache.get(f"email_zip_{token}")
    if not zip_data:
        return HttpResponse('File expired or invalid.', status=404)
    
    response = HttpResponse(zip_data, content_type="application/zip")
    response['Content-Disposition'] = f"attachment; filename={token}.zip"
    return response


@login_required
@permission_required('clientrelations.access_client_relations', raise_exception=True)
def aclient_call_log(request):
    if request.method == 'POST' and 'button_pressed' in request.POST:
        ACLIENT_MONTHLY_CALL_LOG_DIRECTORY = '/mnt/newbiz/AClient/call_report/'
        ACLIENT_QUARTERLY_CALL_LOG_DIRECTORY = '/mnt/newbiz/AClient/call_report/'

        report_period = request.POST.get('period')

        if report_period == "Monthly":
            create_aclient_call_logs("Monthly", ACLIENT_MONTHLY_CALL_LOG_DIRECTORY, )
            messages.success(request, f'AClient Monthly Call Log created in {ACLIENT_MONTHLY_CALL_LOG_DIRECTORY}')
        elif report_period == "Quarterly":
            create_aclient_call_logs("Quarterly", ACLIENT_QUARTERLY_CALL_LOG_DIRECTORY, )
            messages.success(request, f'AClient Quarterly Call Log created in {ACLIENT_QUARTERLY_CALL_LOG_DIRECTORY}')
        else:
            messages.error(request, f'Selected AClient call log period was not an option.')

        return render(request, 'clientrelations/cr_tool_templates/tool_output.html')

    return render(request, 'clientrelations/cr_tool_templates/aclient_call_log.html')


@login_required
@permission_required('clientrelations.access_client_relations', raise_exception=True)
def aclient_file_merger(request):
    if request.method == 'POST' and 'button_pressed' in request.POST:
        ACLIENT_FILE_MERGE_DIRECTORY = '/mnt/newbiz/AClient/remit/'

        data =[]
        for file in os.listdir(ACLIENT_FILE_MERGE_DIRECTORY):
            if file.endswith(".txt") and file.startswith("AClient"):
                aclient_file_merge_dataframe = pd.read_csv(os.path.join(ACLIENT_FILE_MERGE_DIRECTORY, file), header=None)
                data.append(aclient_file_merge_dataframe)

        combined_aclient_dataframes = pd.concat(data, ignore_index=True)

        output_filename = os.path.join(ACLIENT_FILE_MERGE_DIRECTORY, 'output.xlsx')
        combined_aclient_dataframes.to_excel(output_filename, index=False, header=False)

        messages.success(request, f'Files in {ACLIENT_FILE_MERGE_DIRECTORY} have been successfully merged.')

        return render(request, 'clientrelations/cr_tool_templates/tool_output.html')

    return render(request, 'clientrelations/cr_tool_templates/aclient_file_merger.html')


@login_required
@permission_required('clientrelations.access_client_relations', raise_exception=True)
def revo_weekly_invoice(request):
    if request.method == 'POST' and 'button_pressed' in request.POST:
        revo_weekly_invoice_DIRECTORY = '/mnt/newbiz/Revo/remit/Weekly remit recap'

        create_revo_weekly_invoices(revo_weekly_invoice_DIRECTORY)

        messages.success(request, f'Revo weekly invoices created in {revo_weekly_invoice_DIRECTORY}')

        return render(request, 'clientrelations/cr_tool_templates/tool_output.html')

    return render(request, 'clientrelations/cr_tool_templates/revo_weekly_invoice.html')


@login_required
@permission_required('clientrelations.access_client_relations', raise_exception=True)
def sectional_call_logs(request):
    if request.method == 'POST' and 'button_pressed' in request.POST:
        sectional_call_logs_DIRECTORY = '/mnt/newbiz/Sectional/call_report'

        create_sectional_call_logs(sectional_call_logs_DIRECTORY)

        messages.success(request, f'Sectional Call Log successfully created in {sectional_call_logs_DIRECTORY}')

        return render(request, 'clientrelations/cr_tool_templates/tool_output.html')

    return render(request, 'clientrelations/cr_tool_templates/sectional_call_logs.html')
