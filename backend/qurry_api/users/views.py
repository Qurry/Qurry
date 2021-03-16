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
from qurry_api.base import (AuthenticatedView, method_required,
                            object_existence_required)

from .forms import UserCreationForm
from .models import ActivationToken, ResetToken, User, clean_email_address


def new_jwt_token(uid):
    return jwt.encode({
        'token_type': 'access',
        'exp': int(time.time()) + settings.JWT_VALIDITY_PERIOD,
        'jti': secrets.token_urlsafe(15),
        'user_id': str(uid),
    }, settings.SECRET_KEY, algorithm='HS256')


class Accounting(View):
    @method_required('POST')
    def register(self, request):
        form = UserCreationForm(request.POST)
        try:
            if not form.is_valid():
                raise ValidationError()

            user = form.save(commit=False)
            user.is_active = False
            user.save()

            mail_subject = 'Activate your account.'
            message = render_to_string('activation_email.html', {
                'token': ActivationToken().new_for(user),
                'domain': get_current_site(request),
            })
            to_email = form.cleaned_data.get('email')
            send_mail(mail_subject, message, settings.EMAIL_HOST_USER, [
                to_email], html_message=message)

            return JsonResponse({}, status=201)

        except Exception as exc:
            response_json = {'errors': []}
            for field, errors in form.errors.items():
                response_json['errors'].append('%s' % field.join(errors))

            if not response_json['errors']:
                response_json['errors'].append(str(exc))

            return JsonResponse(response_json, status=400)

    @method_required('POST')
    def login(self, request):
        try:
            body = json.loads(request.body.decode('utf-8'))
            email = body['email']
            password = body['password']

            if not email or not password:
                raise ValueError

            email = clean_email_address(email)
            user = User.objects.get(email=email)
            if not user.check_password(password):
                raise PermissionDenied()

            if not user.is_active:
                raise PermissionDenied

        except ValueError:
            return JsonResponse({'errors': ['request must contain email and password as strings']}, status=400)

        except (User.DoesNotExist, PermissionDenied):
            return JsonResponse({'errors': ['This user does not exist, has not confirmed their email or the password is invalid.']}, status=400)

        token = new_jwt_token(user.id)

        return JsonResponse({'access': token})

    @method_required('GET')
    def activate(self, request, uid, token):
        try:
            user = User.objects.get(id=uid)
            token = ActivationToken.objects.get(user=user, value=token)
            if not token.is_valid():
                raise Exception('invalid token')
            token.delete()
            user.is_active = True
            user.save()
            return redirect('/register/success')
        except Exception:
            return redirect('/register/invalid')

    @method_required('POST')
    def forgot_password(self, request):
        try:
            email = json.loads(request.body).get('email')
            user = User.objects.get(email=email)

            mail_subject = 'Reset your password.'
            message = render_to_string('password_reset_email.html', {
                'token': ResetToken().new_for(user),
                'domain': get_current_site(request),
            })

            # send_mail(mail_subject, message, settings.EMAIL_HOST_USER, [
            #     email], html_message=message)

            print(message)

            return JsonResponse({}, status=200)

        except Exception:
            return JsonResponse({'errors': ['invalid email address']}, status=400)

    @method_required('GET')
    def reset_password(self, request, uid, token):
        try:
            user = User.objects.get(id=uid)
            token = ResetToken.objects.get(user=user, value=token)
            if not token.is_valid():
                raise Exception('invalid token')

            response = redirect('home')
            response.set_cookie('validation', token.validation)
            return response
        except Exception:
            # TODO change me
            return redirect('/register/invalid')

    @method_required('POST')
    def set_password(self, request):
        try:
            token = ResetToken.objects.get(
                validation=request.headers.get('validation'))
            if not token.is_valid():
                raise Exception('invalid token')
            user = token.user
            token.delete()

            password = json.loads(request.body).get('password')
            UserCreationForm().validate_password(password)

        except Exception as exc:
            return JsonResponse({'erorrs': [str(exc)]}, 400)

        return JsonResponse({'access': new_jwt_token(user.id)})


class UserView(AuthenticatedView):
    Model = User

    @object_existence_required
    def get(self, request, *args, **kwargs):
        if 'id' in kwargs:
            user = User.objects.get(id=kwargs['id'])
            return JsonResponse(user.as_detailed())

        return JsonResponse(list(user.as_detailed() for user in User.objects.all_active()), safe=False)


class ProfileView(AuthenticatedView):

    def get(self, request, *args, **kwargs):
        return JsonResponse(self.user.profile_info())

    def patch(self, request, *args, **kwargs):
        try:
            self.change(**json.loads(request.body.decode('utf-8') or '{}'))
        except ValidationError as exc:
            return JsonResponse({'errors': extract_errors(exc)}, status=400)
        except Exception as exc:
            return JsonResponse({'errors': [str(exc)]}, status=400)

        return JsonResponse({'userId': self.user.id})

    def change(self, **kwargs):
        if 'username' in kwargs:
            self.user.username = kwargs['username']

        if 'newPassword' in kwargs:
            if not self.user.check_password(kwargs.get('oldPassword')):
                raise PermissionDenied(
                    'your old password is wrong')
            try:
                UserCreationForm().validate_password(kwargs['newPassword'])
            except ValidationError as exc:
                raise ValidationError('{"newPassword": %s}' % str(exc))

            self.user.set_password(kwargs['newPassword'])

        self.user.full_clean()
        self.user.save()
