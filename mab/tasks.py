from config.settings.celery import app

import zipfile, os, base64, json, time
import requests
from celery import shared_task
from datetime import datetime
from urllib.parse import urlencode
from django.conf import settings
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from mab.models import DashboardLink
from mab.utils.email_utils import send_email
from io import StringIO, BytesIO
import csv


@shared_task(bind=True)
def fetch_letter_data(self, search_data):
    base_url = f'http://host.docker.internal:3000/api/letters'

    # Construct the query string 
    query_string = {}
    if search_data.get('startDate'):
        query_string['start_date'] = search_data['startDate']
    if search_data.get('endDate'):
        query_string['end_date'] = search_data['endDate']
    if search_data.get('refnum'):
        query_string['ReferenceNumber'] = search_data['refnum']
    if search_data.get('recieverName'):
        query_string['html_search'] = search_data['recieverName']
    if search_data.get('client'):
        query_string['client'] = search_data['client']
    if search_data.get('page'):
        query_string['page'] = search_data['page']
    if search_data.get('limit'):
        query_string['limit'] = search_data['limit']

    api_url = f"{base_url}?{urlencode(query_string)}"

    try:
        response = requests.get(api_url, headers={ 'x-api-key': os.getenv('API_KEY') })
        response.raise_for_status()
        letter_data = response.json()

        for email_entry in letter_data.get('results', []):  # convert letter date to dateime objects
            email_entry['EmailDate'] = datetime.strptime(
                email_entry['EmailDate'], "%Y-%m-%dT%H:%M:%S.%fZ"
            )
            if email_entry.get('EmailBcc'):  # get client name from BCC
                email_entry['EmailBcc'] = email_entry['EmailBcc'].split('@')[0]
        
        return letter_data

    except requests.exceptions.RequestException as e:
        raise self.retry(exc=e, countdown=60, max_retries=3)
    

@shared_task(autoretry_for=(Exception,), retry_backoff=True, retry_kwargs={'max_retries': 5})
def build_email_zip_for_client(client, date):
    api_url = f'http://host.docker.internal:3000/api/letters_zip?client={client}&start_date={date}&end_date={date}'
    
    # Call Node API to generate email file
    try:
        response = requests.get(api_url, stream=True, headers={ 'x-api-key': os.getenv('API_KEY') })
        response.raise_for_status()

    except Exception as error:
        return {'status': 'error', 'message': str(error)}
    
    # Stream the JSONL file into a zip in memory
    zip_buffer = BytesIO()
    jsonl_stream = response.iter_lines(decode_unicode=True)

    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        # with open(jsonl_path, 'r', encoding='utf-8') as jsonl_file:
        for line_num, line in enumerate(jsonl_stream, 1):
            try:
                email_data = json.loads(line)

                email_datetime = datetime.strptime(email_data['EmailDate'], "%Y-%m-%dT%H:%M:%S.000Z")
                formatted_date = email_datetime.strftime("%a, %d %b %Y %H:%M:%S +0000")

                email_msg = MIMEMultipart()
                email_msg['Subject'] = email_data['EmailSubject']
                email_msg['From'] = email_data['EmailFrom']
                email_msg['To'] = email_data['EmailTo']
                email_msg['Date'] = formatted_date
                email_msg.attach(MIMEText(email_data['HTML'], "html"))

                eml_content = email_msg.as_string()
                eml_filename = f"{email_datetime.strftime('%H%M%S')}_{email_data['EmailSubject']}.eml"
                zip_file.writestr(eml_filename, eml_content)

            except Exception as error:
                print(F'Error creating eml: {error}')
                continue

    zip_buffer.seek(0)
    zip_base64 = base64.b64encode(zip_buffer.read()).decode('utf-8')

    return {
        'status': 'complete',
        'zip_data': zip_base64,
        'filename': f"{client}_{date}.zip",
    }


@app.task
def TEST_export_dashboard_links():
    file_path = ''

    dashboard_links = DashboardLink.objects.all()

    csv_data = StringIO()
    csv_writer = csv.writer(csv_data)
    csv_writer.writerow(['Name', 'Description', 'Link', 'Department', 'Type'])
    for link in dashboard_links:
        csv_writer.writerow([link.name, link.description, link.link, link.get_department_disply(), link.get_type_display()])

    with open(file_path, 'w', newline='') as file:
        file.write(csv_data.getvalue())
