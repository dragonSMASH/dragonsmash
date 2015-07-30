import json
from django.http import HttpResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from api.serializers import RegisterPlayerResource


@api_view(['GET'])
@permission_classes((AllowAny,))
def status(request):
    response_data = {'message': 'howdy, partner!'}
    return HttpResponse(json.dumps(response_data), content_type="application/json")


@api_view(['POST'])
@permission_classes((AllowAny,))
def register(request):
    register_info = RegisterPlayerResource(data=request.data)
    if register_info.is_valid(raise_exception=True):
        player = register_info.save()
        return Response({"player_id": player.id, "auth_token": player.user.auth_token.key})


@api_view(['POST'])
def logout(request):
    request.user.auth_token.delete()
    return Response({"message": "logout successful"})


def exception_handler(exception, context):
    """ Return well-formed and consistent response in case any exceptions occur """
    response = {}
    if hasattr(exception, "detail"):
        response["message"] = exception.detail
    elif hasattr(exception, "messages"):
        response["message"] = exception.messages
    else:
        response["message"] = "unknown error occurred"
    return Response(response)
