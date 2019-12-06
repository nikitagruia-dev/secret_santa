import traceback
from collections.abc import Iterable

from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.permissions import AllowAny

schema_view = get_schema_view(
    openapi.Info(
        title="API Documentation",
        default_version='v1',
        description="Enjoy",
    ),
    validators=['ssv'],
    public=True,
    permission_classes=(AllowAny,)
)


def send_html_message(emails: list, title: str, template_path: str, context: dict) -> None:
    """
    Send email by text template
    :param title: title message
    :param emails: list of receivers
    :param template_path: path to template, from templates/emails folder
    :param context: some context for template
    :return: boolean value
    Example : send_html_message(
                                ["iurii.ebs@gmail.com", ],
                                "Title test",
                                "emails/template_message.html",
                                {"test_text": "test test test"}
                                )
    """
    if isinstance(emails, str) or not isinstance(emails, Iterable):
        emails = [emails]
    html = render_to_string(template_path, context)

    msg = EmailMessage(
        title,
        html,
        to=emails,
        from_email='Santa <%s>' % settings.EMAIL_HOST_USER
    )
    msg.content_subtype = 'html'
    try:
        msg.send()
    except Exception:
        traceback.print_exc()

