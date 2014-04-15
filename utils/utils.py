from armadillo_reuse.settings import EMAIL_HOST, EMAIL_HOST_PASSWORD, EMAIL_HOST_USER, EMAIL_PORT, EMAIL_USE_TLS, GCM_API_KEY
import pyzmail
import requests
import jsonpickle
from web_api.models import GcmUser

def send_mail(sender, recipients, subject, text_content, headers=[]):
    """
    Sends email using pyzmail
    """
    prefered_encoding = 'iso-8859-1'
    text_encoding = 'iso-8859-1'

    smtp_host = EMAIL_HOST
    smtp_port = EMAIL_PORT
    smtp_mode = 'tls' if EMAIL_USE_TLS else 'normal'
    smtp_login = EMAIL_HOST_USER if EMAIL_HOST_USER != '' else None
    smtp_password = EMAIL_HOST_PASSWORD if EMAIL_HOST_USER != '' else None

    payload, mail_from, rcpt_to, msg_id = pyzmail.compose_mail(
        ("Reuse Mobile", sender),
        recipients,
        subject,
        prefered_encoding,
        (text_content, text_encoding),
        html=None, headers=headers)

    ret = pyzmail.send_mail(payload, mail_from, rcpt_to, smtp_host, smtp_port=smtp_port, smtp_mode=smtp_mode,
                            smtp_login=smtp_login, smtp_password=smtp_password)


    if isinstance(ret, dict):
        if ret:
            return 'failed recipients:' + ','.join(ret.keys())
        else:
            return 'success'
    else:

        return 'error: ' + ret + "\n\n "+ ' from: ' + mail_from + " host: " +smtp_host+" port: "+ str(smtp_port) + " mode: " + smtp_mode + " login: " + str(smtp_login) + " password: " + str(smtp_password)

def send_gcm_message(reg_ids, data, collapse_key):
    """Sends gcm message to devices in reg_ids
    returns the json response from the gcm server
    """

    message = {
        'registration_ids': reg_ids,
        'collapse_key': collapse_key,
        'data': data
    }

    message = jsonpickle.encode(message)

    headers = {
        'UserAgent': "GCM-Server",
        'Content-Type': 'application/json',
        'Authorization': 'key=' + GCM_API_KEY,
    }

    response = requests.post(url="https://android.googleapis.com/gcm/send",
                             data=message,
                             headers=headers)
    return response.status_code

def notify_all_users():
    #Notify all clients of change, pull from server
    data = {'action' : 'pull'}
    reg_ids = []
    for entry in GcmUser.objects.all():
        reg_ids.append(entry.gcm_id)
    res = send_gcm_message(reg_ids, data, 'pull')
    #return res
