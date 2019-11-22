from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
def send_invite_email(link, emails):
    subject = "LinkUp Event Invite"
    from_email = 'LinkUp.com'
    to = emails
    text = "You've been invited to join an event on LinkUp! Please click the link below to join." + '\n' +link
    msg = EmailMultiAlternatives(subject, text, from_email, [to])
    msg.send()