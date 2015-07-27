import json
from django.http import HttpResponse


# Create your views here.
def status(request):
    response_data = {'message': 'howdy, partner!'}
    return HttpResponse(json.dumps(response_data), content_type="application/json")


def register(request):
    response_data = {'result': 'failed', 'message': 'You messed up'}
    return HttpResponse(json.dumps(response_data), content_type="application/json")
