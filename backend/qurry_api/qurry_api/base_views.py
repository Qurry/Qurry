from django.views import View
from rest_framework_simplejwt.authentication import JWTAuthentication

class AthenticatedView(View):
    def setup(self, request, *args, **kwargs):
        user, token = JWTAuthentication().authenticate(request)
        if user:
            self.user = user
        return super().setup(request, *args, **kwargs)