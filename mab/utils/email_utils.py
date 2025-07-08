import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from typing import List, Dict, Union

def send_email_with_attachment(reciepent_emails, subject, body, attachment_paths, sender_email='tech@business.com', cc_emails=''):    
    # create multipart message
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = '. '.join(reciepent_emails)
    message['Subject'] = subject

    if cc_emails:
         message['Cc'] = '. '.join(cc_emails)

    # attach the body of the email
    message.attach(MIMEText(body, 'plain'))

    # attach the files
    for attachment_path in attachment_paths:
        attachment = open(attachment_path, 'rb')
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(attachment_path)}')
        message.attach(part)

    # connect to the SMTP server
    with smtplib.SMTP("192.168.4.39") as server:
            server.sendmail(sender_email, reciepent_emails, message.as_string())


def send_email(
         subject: str,
         body: str,
         to: List[str],
         from_email: str = 'tech@business.com',
         cc: List[str] = None,
         bcc: List[str] = None,
         attachments: List[Union[str, Dict[str, Union[str, bytes]]]] = None,
         html: bool = False,
         smtp_host: str = "192.168.4.39",
         smtp_port: int = 25,
         headers: Dict[str, str] = None,
):
    """
    Send an email with optional attachments, CC, BCC, and HTML/plain body.

    Args:
       subject: Email subject
       body: Email body (plain or html)
       to: List of recipient emails
       from_email: Sender's email
       cc: Optional list of CC emails
       bcc: Optional list of BCC emails
       attachments: List of file paths or dicts like {'filename': str, 'content': bytes}
       html: Whether body should be sent as HTML
       smtp_host: SMTP server
       smtp_port: SMTP port
       headers: Optional additional headers 
    """
    cc = cc or []
    bcc = bcc or []
    attachments = attachments or []
    headers = headers or {}

    msg = MIMEMultipart
    msg['From'] = from_email
    msg['To'] = ', '.join(cc)
    msg['Subject'] = subject

    if cc:
        msg['Cc'] = ', '.join(cc)
    
    for key, value in headers.items():
        msg[key] = value

    msg.attach(MIMEText(body, 'html' if html else 'plain'))

    for attachment in attachments:
        if isinstance(attachment, str):
            # it's a filpath
            with open(attachment, 'rb') as f:
                 content = f.read()
                 filename = os.path.basename(attachment)
        elif isinstance(attachment, dict):
            content = attachment['content']
            filename = attachment['filename']
        else:
            raise ValueError("Attachments must be file paths or dicts with 'filename' and 'content'.")
        
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(content)
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename={filename}')
        msg.attach(part)

    all_recipients = to + cc + bcc
    with smtplib.SMTP(smtp_host, smtp_port) as server:
         server.sendmail(from_email, all_recipients, msg.as_string())
    
