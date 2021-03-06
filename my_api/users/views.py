from __future__ import absolute_import, unicode_literals


from django.contrib.auth import login

from django.http import JsonResponse
from social.apps.django_app.utils import psa
 
from .tools import get_access_token


_ERROR_TOKEN_EXCHANGE_RESPONSE = JsonResponse(
    {
        "error": "unsuccessful_token_exchange",
        "error_description": "Unable to complete token exchange with social backend."
    },
    status=401
)


@psa('social:complete')
def register_by_access_token(request, backend):
    token = request.GET.get('access_token')
    username = request.GET.get('username', None)

    # We pass the parameters to the backend so it can make the appropriate requests to the third party site.
    user = request.backend.do_auth(token, username=username)

    if user:
        try:
            login(request, user)
        except Exception:
            return _ERROR_TOKEN_EXCHANGE_RESPONSE
        else:
            return get_access_token(user)
    else:
        return _ERROR_TOKEN_EXCHANGE_RESPONSE