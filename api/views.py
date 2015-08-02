from django.conf import settings
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.views import exception_handler
from .serializers import RegisterPlayerResource


# Convenience decorators for get-only and post-only view
def api_get_view(func):
    return api_view()(func)


def api_post_view(func):
    return api_view(['POST'])(func)


# API-wide exception handler (Set in config.settings.base)
def handle_exception(exception, context):
    """ Return well-formed and consistent response in case any exceptions occur """
    response = exception_handler(exception, context)
    data = {}
    if hasattr(exception, "detail"):
        data["message"] = exception.detail
    elif hasattr(exception, "messages"):
        data["message"] = exception.messages
    else:
        data["message"] = "unknown error occurred"

    # add in the default text if we're debugging and not testing
    if settings.DEBUG and not settings.TEST:
        data["extra"] = response.data

    response.data = data
    return response


# Main API Views
@api_get_view
@permission_classes((AllowAny,))
def status(request):
    response_data = {'message': 'howdy, partner!'}
    return Response(response_data)


@api_post_view
@permission_classes((AllowAny,))
def register(request):
    register_info = RegisterPlayerResource(data=request.data)
    if register_info.is_valid(raise_exception=True):
        player = register_info.save()
        return Response({"player_id": player.id, "auth_token": player.user.auth_token.key})


@api_post_view
def logout(request):
    request.user.auth_token.delete()
    return Response({"message": "logout successful"})
