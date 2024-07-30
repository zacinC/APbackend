from __future__ import print_function
from datetime import datetime, timedelta, timezone
import jwt
from passlib.context import CryptContext
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
import logging

from ..schemas.schemas import UserBase
from ..settings import EMAIL_RESET_TOKEN_EXPIRE_HOURS, SECRET_KEY, BREVO_API_KEY


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password_reset_token(token: str) -> str | None:
    try:
        decoded_token = jwt.decode(
            token, SECRET_KEY, algorithms=["HS256"])
        return str(decoded_token["sub"])
    except jwt.InvalidTokenError:
        return None


def generate_password_reset_token(email: str) -> str:
    delta = timedelta(hours=EMAIL_RESET_TOKEN_EXPIRE_HOURS)
    now = datetime.now(timezone.utc)
    expires = now + delta
    exp = expires.timestamp()
    encoded_jwt = jwt.encode(
        {"exp": exp, "nbf": now, "sub": email},
        SECRET_KEY,
        algorithm="HS256",
    )
    return encoded_jwt


def generate_password_reset_email(user: UserBase):
    project_name = "Autobuski Prevoz Crne Gore"
    subject = f"{project_name} - Password recovery for user {user.email}"

    token = generate_password_reset_token(user.username)
    context = {
        "project_name": project_name,
        "username": user.username,
        "email": user.email,
        "valid_hours": EMAIL_RESET_TOKEN_EXPIRE_HOURS,
        "link": f'localhost:8000/recover-password/{token}'
    }

    html_content = render_email_template(context=context)

    return {"subject": subject, "html_content": html_content}


def render_email_template(context: dict) -> str:
    html_content = f"""
    <html>
      <body>
        <p>Dear {context["username"]},</p>
        <p>
          You have requested to reset your password for the project {context["project_name"]}.
          Click the link below to reset your password:
        </p>
        <p><a href="{context["link"]}">Reset Password</a></p>
        <p>This link will expire in {context["valid_hours"]} hours.</p>
        <p>If you did not request this password reset, please ignore this email.</p>
      </body>
    </html>
    """
    return html_content


def send_email(user: UserBase, html_content, subject):
    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key['api-key'] = BREVO_API_KEY

    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(
        sib_api_v3_sdk.ApiClient(configuration))
    sender = {"name": "APCG", "email": "dbzvegetassj@outlook.com"}
    to = [{"email": user.email, "name": user.full_name}]
    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
        to=to, html_content=html_content, sender=sender, subject=subject)

    try:
        api_response = api_instance.send_transac_email(send_smtp_email)
        logging.info(f'API response: {api_response}')
        logging.info(f'Mail sent to {user.email}')

    except ApiException as e:
        print(
            "Exception when calling SMTPApi->send_transac_email: %s\n" % e)
