import logging

from django.apps import apps as django_apps
from django.conf import settings
from django.utils.encoding import force_str
from django.utils.translation import gettext as _
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication, get_authorization_header


logger = logging.getLogger(__name__)


class JSONWebTokenAuthentication(BaseAuthentication):
    """Token based authentication using the JSON Web Token standard."""

    def authenticate(self, request):
        """Entrypoint for Django Rest Framework"""
        jwt_token = self.get_jwt_token(request)
        if jwt_token is None:
            return None


    # def get_user_model(self):
    #     user_model = getattr(settings, "COGNITO_USER_MODEL", settings.AUTH_USER_MODEL)
    #     return django_apps.get_model(user_model, require_ready=False)

    def get_jwt_token(self, request):
        auth = get_authorization_header(request).split()
        if not auth:
           return None
            
        if len(auth) == 0:
            msg = _("Invalid Authorization header. No credentials provided.")
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) >= 2:
            msg = _(
                "Invalid Authorization header. Credentials string "
                "should not contain spaces."
            )
            raise exceptions.AuthenticationFailed(msg)

        return auth[0]

    
   