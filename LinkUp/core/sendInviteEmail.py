from django.core.mail import send_mail

def send_invite_email(link, emails):
    subject = "LinkUp Event Invite"
    from_email = 'linkup@gmail.com'
    to = emails
    text = "You've been invited to join an event on LinkUp! Please click the link below to join."
    html_link = render_to_string(inviteLink.html, {'pk': link})

    msg = EmailMultiAlternatives(subject, text, from_email, [to])
    msg.attach_alternative(html_link, "text/html")
    msg.send()