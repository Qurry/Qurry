from django.views import View
from rest_framework_simplejwt.authentication import JWTAuthentication


class AuthenticatedView(View):
    def setup(self, request, *args, **kwargs):
        self.user = None
        user_token = JWTAuthentication().authenticate(request)
        if user_token:
            self.user = user_token[0]
        return super().setup(request, *args, **kwargs)
