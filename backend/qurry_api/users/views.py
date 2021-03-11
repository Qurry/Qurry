import json
import secrets
import time

import jwt
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import PermissionDenied, ValidationError
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.views import View
from questions.views import extract_errors
from qurry_api.base import (AuthenticatedView, authenticate_user,
                            method_required, object_existence_required)

from .forms import UserCreationForm
from .models import ActivationToken, User


class Accounting(View):
    @method_required('POST')
    def register(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            mail_subject = 'Activate your account.'
            message = render_to_string('email_template.html', {
                'user': user,
                'uid': user.id,
                'token': ActivationToken.token_for(user),
                'domain': get_current_site(request),
            })
            to_email = form.cleaned_data.get('email')
            send_mail(mail_subject, message, settings.EMAIL_HOST_USER, [
                to_email], html_message=message)

            return JsonResponse({}, status=201)
        else:
            response_json = {'errors': {}}
            for field, errors in form.errors.items():
                response_json['errors'][field] = ' '.join(errors)

            return JsonResponse(response_json, status=409)

    @method_required('POST')
    def login(self, request):
        try:
            body = json.loads(request.body.decode('utf-8'))
            email = body['email']
            password = body['password']

            if not email or not password:
                raise ValueError

            user = User.objects.get(email=email)
            if not user.check_password(password):
                raise PermissionDenied()

            if not user.is_active:
                raise PermissionDenied

        except ValueError:
            return JsonResponse({'errors': ['request must contain email and password as strings']}, status=400)

        except (User.DoesNotExist, PermissionDenied):
            return JsonResponse({'errors': ['This user does not exist, has not confirmed their email or the password is invalid.']}, status=400)

        token = jwt.encode({
            'token_type': 'access',
            'exp': int(time.time()) + settings.JWT_VALIDITY_PERIOD,
            'jti': secrets.token_urlsafe(15),
            'user_id': str(user.id),
        }, settings.SECRET_KEY, algorithm='HS256')

        return JsonResponse({'access': token})

    @method_required('GET')
    def activate(self, request, uid, token):
        try:
            user = User.objects.get(id=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and ActivationToken.is_token_valid_for(user, token):
            user.is_active = True
            user.save()
            return redirect('/register/success')
        else:
            return redirect('/register/invalid')


class UserView(AuthenticatedView):
    Model = User
    mode = None

    @object_existence_required
    def get(self, *args, **kwargs):
        if 'id' in kwargs:
            user = User.objects.get(id=kwargs['id'])
            return JsonResponse(user.as_detailed())

        return JsonResponse(list(user.as_detailed() for user in User.objects.all_active()), safe=False)

    @authenticate_user
    def profile(self, request):
        if request.method == 'GET':
            return JsonResponse(self.user.profile_info())
        if request.method == 'PATCH':
            try:
                self.change(**json.loads(request.body.decode('utf-8') or '{}'))
            except ValidationError as exc:
                return JsonResponse({'errors': extract_errors(exc)}, status=400)
            except Exception as exc:
                return JsonResponse({'errors': [str(exc)]}, status=400)

            return JsonResponse({'userId': self.user.id})
        else:
            return JsonResponse({'errors': ['if you need to edit your profile, PATCH to profile/']}, status=405)

    def change(self, **kwargs):
        if 'username' in kwargs:
            self.user.username = kwargs['username']

        if 'newPassword' in kwargs:
            if not self.user.check_password(kwargs.get('oldPassword')):
                raise PermissionDenied(
                    'your old password is wrong or you did not send it')
            try:
                UserCreationForm().validate_password(kwargs['newPassword'])
            except ValidationError as exc:
                print('{"newPassword": %s}' % exc)
                raise ValidationError('{"newPassword": %s}' % str(exc))

            self.user.set_password(kwargs['newPassword'])

        self.user.full_clean()
        self.user.save()
