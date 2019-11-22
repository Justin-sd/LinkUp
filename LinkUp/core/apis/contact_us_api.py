from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
def send_contact_email(name, email, message):
    subject = "Contact Us Email"
    from_email = 'LinkUp.com'
    to = 'linkupmeeting@gmail.com'
    text = name + " says " + message + '\n' + '\n' + "To respond, email:" + '\n' + email
    msg = EmailMultiAlternatives(subject, text, from_email, [to])
    msg.send()