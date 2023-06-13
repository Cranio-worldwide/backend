from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken


def send_verification_email(request, user, language):
    token = RefreshToken.for_user(user).access_token
    current_site = get_current_site(request).domain
    url_path = reverse('verify_email')
    absurl = 'http://' + current_site + url_path + '?token=' + str(token)
    subject = settings.EMAIL_DATA.get(language)['EMAIL_SUBJECT']
    text = settings.EMAIL_DATA.get(language)["EMAIL_MESSEGE"]

    email_body = (
        f'{user.email} \n'
        f'{text} \n' + absurl
    )

    email = EmailMessage(
        to=[user.email],
        subject=subject,
        body=email_body
    )
    email.send()
