
from string import Template
import smtplib  # for error handle
from pathlib import Path
from django.core.mail import send_mail

# use Template over `{}`-format to prevent getting
# confused with JS's block syntax.
MSG = Template("欢迎报名爱特工作室，你的验证码是：$code")
def slurp(fn):
    f = open(fn, encoding="utf-8")
    res = f.read()
    return res

H_MSG = Template(
    slurp(
        Path(__file__).with_name("verify_code.html")
    ))

def send_code(code, emails):
    """returns None is not error (successful).
    If error occurs, returns error message (str).
    """
    num_sent = 0
    err_msg = "success"
    try:
        num_sent = send_mail(
            '报名验证', MSG.substitute(code=code),
            None, # None means using the value of DEFAULT_FROM_EMAIL setting
            emails,
            html_message=H_MSG.substitute(code=code))
    except smtplib.SMTPServerDisconnected:
        err_msg = "SMTP server disconnected"
    except smtplib.SMTPResponseException as e:
        err_msg = e.smtp_error
        if type(err_msg) is bytes:
            err_msg = err_msg.decode()
    except smtplib.SMTPException as e:
        err_msg = "error"
    if num_sent != 0:
        return None
    return err_msg
