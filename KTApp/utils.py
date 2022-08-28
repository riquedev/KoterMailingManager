import socket
from rest_framework.permissions import BasePermission
from rest_framework.permissions import IsAuthenticated
from rest_framework_api_key.permissions import HasAPIKey
from .permissions import APIIsEnabled


def host_is_local(hostname, port=None):
    """returns True if the hostname points to the localhost, otherwise False."""
    if port is None:
        port = 22  # no port specified, lets just use the ssh port
    hostname = socket.getfqdn(hostname)
    if hostname in ("localhost", "0.0.0.0"):
        return True
    localhost = socket.gethostname()
    localaddrs = socket.getaddrinfo(localhost, port)
    targetaddrs = socket.getaddrinfo(hostname, port)
    for (family, socktype, proto, canonname, sockaddr) in localaddrs:
        for (rfamily, rsocktype, rproto, rcanonname, rsockaddr) in targetaddrs:
            if rsockaddr[0] == sockaddr[0]:
                return True
    return False


def get_rest_permissions() -> list[BasePermission]:
    return [
        APIIsEnabled, IsAuthenticated | HasAPIKey
    ]
