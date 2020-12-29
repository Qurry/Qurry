from django.views import View
from rest_framework_simplejwt.authentication import JWTAuthentication

class AthenticatedView(View):
    def setup(self, request, *args, **kwargs):
        user_token = JWTAuthentication().authenticate(request)
        if user_token:
            self.user = user_token[0]
        else:
            self.user = None
        return super().setup(request, *args, **kwargs)