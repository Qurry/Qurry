import jwt
import base64
import six

from django.views import View
from django.http import JsonResponse
from django.contrib.admin.options import BaseModelAdmin
from django.core.exceptions import PermissionDenied
from django.db.models import ImageField
from django.utils.safestring import mark_safe
from django.contrib.auth.models import update_last_login
from django.conf import settings

from users.models import User
from users.backends import JWTAuthentication


def ownership_required(function):
    def is_owner(self, *args, **kwargs):
        if 'id' in kwargs:
            obj = self.Model.objects.get(id=kwargs['id'])
            if not self.user.is_owner_of(obj):
                raise PermissionDenied(
                    'you have to own the %s object to be able to do this action' % self.Model.__name__)
            return function(self, *args, **kwargs)

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


def admin_thumbnail(field_name, *args, **kwargs):
    label = kwargs.get('label', settings.ADMIN_THUMBNAIL_DEFAULT_LABEL)

    def _model_admin_wrapper(admin_class):
        if not issubclass(admin_class, BaseModelAdmin):
            raise ValueError(
                'admin_thumbnails: Wrapped class must be a subclass of django.contrib.admin.options.BaseModelAdmin'
            )

        def unpack_styles(styles):
            return '; '.join([': '.join(i) for i in six.iteritems(styles)])

        def thumbnail_field(self, obj):
            field = obj._meta.get_field(field_name)
            field_value = getattr(obj, field_name)
            if not field_value:
                return ''

            if isinstance(field, ImageField):
                file_data = base64.b64encode(
                    field_value.read()).decode('ascii')
            else:
                raise TypeError(
                    'admin_thumbnails: Specified field must be an instance of Django’s `ImageField`(received: {0})'.format(
                        field.get_internal_name())
                )

            style = dict(settings.ADMIN_THUMBNAIL_STYLE)
            return mark_safe(
                '<img src="data:image;base64,{0}" style="{1}" alt="Thumbnail">'.format(
                    file_data, unpack_styles(style))
            )
        thumbnail_field.short_description = label

        new_field_name = '{0}{1}'.format(field_name,
                                         settings.ADMIN_THUMBNAIL_FIELD_SUFFIX)
        setattr(admin_class, new_field_name, thumbnail_field)
        admin_class.readonly_fields = admin_class.readonly_fields + \
            (new_field_name, )
        return admin_class

    return _model_admin_wrapper


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

        update_last_login(None, self.user)
        return super().dispatch(request, request, *args, **kwargs)
