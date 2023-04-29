import requests


def send_email(receiver_email, email_text):
    return requests.post(
        "https://api.mailgun.net/v3/sandbox9314c2d62d36428c9613ddb8502c3427.mailgun.org/messages",
        auth=("api", "11453e79dfd5cfec9838121191da10ab-48c092ba-4e6f8c1a"),
        data={"from": "Mailgun@sandbox9314c2d62d36428c9613ddb8502c3427.mailgun.org",
              "to": [receiver_email],
              "subject": "Advertisement Status",
              "text": email_text})



