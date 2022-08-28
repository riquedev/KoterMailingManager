from django.http import HttpRequest
from ipware import get_client_ip


class KTApi:

    @classmethod
    def notify_insecure_request(cls, request: HttpRequest):
        client_ip, is_routable = get_client_ip(request)
        print(client_ip, is_routable)
