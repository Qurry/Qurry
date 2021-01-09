import jwt

from django.views import View
from django.http import JsonResponse

from users.models import User
from users.backends import JWTAuthentication


class AuthenticatedView(View):
    def dispatch(self, request, *args, **kwargs):
        try:    
            self.user = JWTAuthentication().authenticate(request)
        except (jwt.exceptions.InvalidSignatureError, User.DoesNotExist) as exc:
            return JsonResponse({'errors': ['invalid access token or user does not exist']}, status=401)
        except Exception as exc:
            return JsonResponse({'errors': [str(exc)]}, status=400)

        if not self.user:
            return JsonResponse({'errors': ['you have to login to do this action']}, status=401)
            
        return super().dispatch(request, request, *args, **kwargs)

