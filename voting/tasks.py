from celery import shared_task
from django.core.mail import EmailMessage
from django.conf import settings


@shared_task
def sendEmailTask(data):
    try:
        # print("done")
        sub = data.get('sub')
        msg = data.get('msg')
        msg_to = data.get('msg_to')

        print(sub, msg, msg_to)
        print(data)
        email = EmailMessage(
            sub,  # subject
            msg,  # body
            settings.EMAIL_HOST_USER,  # sender
            [msg_to],  # recievers
        )
        email.fail_silently = False
        email.send()
        return None
    except Exception as e:
        print(e)
