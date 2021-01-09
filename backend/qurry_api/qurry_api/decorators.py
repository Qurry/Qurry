from django.core.exceptions import PermissionDenied
from django.http import JsonResponse

from users.models import User

def ownership_required(function):
    def is_owner(self, obj, *args, **kwargs):
        if not self.user.is_owner_of(obj):
            raise PermissionDenied(
                'you have to own the %s object to be able to do this action' % self.Model.__name__)
        return function(self, obj, *args, **kwargs)

    return is_owner


def object_existence_required(function):
    def does_exist(self, *args, **kwargs):
        if 'id' in kwargs:
            try:
                self.Model.objects.get(id=kwargs['id'])
            except Exception as err:
                return JsonResponse({'errors': [str(err)]}, status=404)
        return function(self, *args, **kwargs)

    return does_exist

def active_user_existence_required(function):
    def does_active_exist(self, *args, **kwargs):
        if 'id' in kwargs:
            try:
                User.objects.get(id=kwargs['id'], is_active=True)
            except Exception as err:
                return JsonResponse({'errors': [str(err)]}, status=404)
        return function(self, *args, **kwargs)

    return does_active_exist