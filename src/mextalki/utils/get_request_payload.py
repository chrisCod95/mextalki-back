import json


def get_request_payload(request):
    return json.loads(request.body.decode('utf-8'))
