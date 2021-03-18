from django.views import View

from .decorators import authenticate_user, with_request_body_decoded


class BaseView(View):
    @authenticate_user
    @with_request_body_decoded
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, request, *args, **kwargs)
