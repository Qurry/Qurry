from django.views import View

from .decorators import authenticate_user, with_request_body_decoded


def error_list_from(error_dict):
    return list(error.as_text() for error in dict(error_dict).values())


class BaseView(View):
    @authenticate_user
    @with_request_body_decoded
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, request, *args, **kwargs)
