import logging

from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):

    response = exception_handler(exc, context)

    if response is None:
        logger.error(f"Critical error: {exc}", exc_info=True)

        return Response(
            {
                "status": "error",
                "code": "server_error",
                "message": "An internal server error occurred. Our team is working to resolve it.",  # noqa: E501
                "details": str(exc) if settings.DEBUG else None,
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    if response.status_code == 403:
        user = context["request"].user
        logger.warning(f"Access denied for user: {user} at {context['view']}")

    custom_response_data = {
        "status": "error",
        "code": response.status_text.lower().replace(" ", "_"),
        "message": "Request execution failed.",
        "details": response.data,
    }

    response.data = custom_response_data
    return response
