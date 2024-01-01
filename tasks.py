import os
import requests
from dotenv import load_dotenv
import jinja2

load_dotenv()

DOMAIN = os.getenv("MAILGUN_DOMAIN")
template_loader = jinja2.FileSystemLoader("templates")
template_env = jinja2.Environment(loader=template_loader)

def render_template(template_file, **context):
    return template_env.get_template(template_file).render(**context)

def send_simple_message(to: str, subject: str, body: str, html):
    return requests.post(
        f"https://api.mailgun.net/v3/{DOMAIN}/messages",
        auth=("api", os.getenv("MAILGUN_API_KEY")),
        data={"from": f"Excited User <mailgun@{DOMAIN}>",
            "to": [to],
            "subject": subject,
            "text": body,
            "html": html
            })

def send_user_registration_email(email: str, username: str):
    return send_simple_message(
        email,
        "Successfully signed up",
        f"Hi {username}. You have seccessfully signed up to the Stores REST API.",
        render_template("email/action.html", username=username)
    )