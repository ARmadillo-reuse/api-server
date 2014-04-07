from armadillo_reuse.settings import EMAIL_HOST, EMAIL_HOST_PASSWORD, EMAIL_HOST_USER, EMAIL_PORT, EMAIL_USE_TLS
import pyzmail


def send_mail(sender, recipients, subject, text_content):
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
        sender,
        recipients,
        subject,
        prefered_encoding,
        (text_content, text_encoding),
        html=None)

    ret = pyzmail.send_mail(payload, mail_from, rcpt_to, smtp_host, smtp_port=smtp_port, smtp_mode=smtp_mode,
                            smtp_login=smtp_login, smtp_password=smtp_password)

    if isinstance(ret, dict):
        if ret:
            return 'failed recipients:' + ','.join(ret.keys())
        else:
            return 'success'
    else:
        return 'error: ' + ret