from abc import abstractmethod

from django.http.response import JsonResponse
from django.views import View

from .decorators import (authenticate_user, object_existence_required,
                         with_request_body_decoded)


def error_list_from(error_dict):
    return list(error.as_text()[2:] for error in dict(error_dict).values())


class BaseView(View):
    @authenticate_user
    @with_request_body_decoded
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        if 'id' in kwargs:
            return self.get_object(request, *args, **kwargs)

        try:
            return self.view_list(**({**request.GET.dict(), **kwargs}))
        except Exception:
            return JsonResponse({'errors': ['get arguments are invalid']}, status=400)

    @ object_existence_required
    def get_object(self, request, *args, **kwargs):
        obj = self.Model.objects.get(id=kwargs['id'])
        if request.GET and self.ActionForm:
            form = self.ActionForm(request.GET.dict(), obj, self.user)
            if form.is_valid():
                form.save()
            else:
                return JsonResponse({'errors': error_list_from(form.errors)}, status=400)
        return self.view_detailed(obj)

    @ abstractmethod
    def view_detailed(self, obj):
        pass

    @ abstractmethod
    def view_list(self, **kwargs):  # in preview format
        pass
