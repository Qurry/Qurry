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
from qurry_api.decorators import (method_required, object_existence_required,
                                  with_request_body_decoded)
from qurry_api.views import BaseView, error_list_from

from .forms import (AuthenticationForm, PasswordForgotForm, PasswordResetForm,
                    RegistrationForm, TokenValidationForm)
from .models import ActivationToken, ResetToken, User


def new_jwt_token(uid):
    return jwt.encode({
        'token_type': 'access',
        'exp': int(time.time()) + settings.JWT_VALIDITY_PERIOD,
        'jti': secrets.token_urlsafe(15),
        'user_id': str(uid),
    }, settings.SECRET_KEY, algorithm='HS256')


class Accounting(View):
    @method_required('POST')
    @with_request_body_decoded
    def register(self, request):
        form = RegistrationForm(request.body)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
        else:
            return JsonResponse({'errors': error_list_from(form.errors)}, status=400)

        try:
            mail_subject = 'Activate your account.'
            message = render_to_string('activation_email.html', {
                'token': ActivationToken().new_for(user),
                'domain': get_current_site(request),
            })
            to_email = form.cleaned_data.get('email')
            send_mail(mail_subject, message, settings.EMAIL_HOST_USER, [
                to_email], html_message=message)

            return JsonResponse({}, status=201)

        except Exception:
            return JsonResponse({'errors': ['Error occured while sending an email']}, status=500)

    @method_required('POST')
    @with_request_body_decoded
    def login(self, request):
        form = AuthenticationForm(data=request.body)
        if form.is_valid():
            return JsonResponse({'access': new_jwt_token(form.get_user().id)})

        return JsonResponse({'errors': error_list_from(form.errors)}, status=400)

    @method_required('GET')
    def activate(self, request, uid, token):
        form = TokenValidationForm(
            {'uid': uid, 'token': token}, ActivationToken)
        if form.is_valid():
            form.get_token().delete()
            user = form.get_user()
            user.is_active = True
            user.save()
            return redirect('/register/success')

        return redirect('/register/invalid')

    @method_required('POST')
    @with_request_body_decoded
    def forgot_password(self, request):
        form = PasswordForgotForm(request.body)
        if form.is_valid():
            user = form.user
        else:
            return JsonResponse({'errors': error_list_from(form.errors)}, status=400)
        try:
            mail_subject = 'Reset your password.'
            message = render_to_string('password_reset_email.html', {
                'token': ResetToken().new_for(user),
                'domain': get_current_site(request),
            })

            send_mail(mail_subject, message, settings.EMAIL_HOST_USER, [
                user.email], html_message=message)

            return JsonResponse({}, status=200)
        except Exception:
            return JsonResponse({'errors': ['Error occured while sending an email']}, status=500)

    @method_required('GET')
    def reset_password(self, request, uid, token):
        form = TokenValidationForm({'uid': uid, 'token': token}, ResetToken)
        if form.is_valid():
            token = form.get_token()
            response = redirect('/password/reset')
            response.set_cookie('validation', token.validation)
            token.got_used()
            return response

        return redirect('/password/invalid')

    @method_required('POST')
    @with_request_body_decoded
    def set_password(self, request):
        password = request.body.get('password')
        validation = request.COOKIES.get('validation')
        form = PasswordResetForm(
            {'validation': validation, 'password': password})

        if form.is_valid():
            user = form.get_user()
            user.set_password(password)
            user.save()

            token = form.get_token()
            token.delete()
        else:
            return JsonResponse({'erorrs': error_list_from(form.errors)}, status=400)

        return JsonResponse({'access': new_jwt_token(user.id)})


class UserView(BaseView):
    Model = User

    @ object_existence_required
    def get(self, request, *args, **kwargs):
        if 'id' in kwargs:
            user = User.objects.get(id=kwargs['id'])
            return JsonResponse(user.as_detailed())

        return JsonResponse(list(user.as_detailed() for user in User.objects.all_active()), safe=False)


class ProfileView(BaseView):

    def get(self, request, *args, **kwargs):
        return JsonResponse(self.user.profile_info())

    def patch(self, request, *args, **kwargs):
        try:
            self.change(request.body)
        except ValidationError as exc:
            return JsonResponse({'errors': extract_errors(exc)}, status=400)
        except Exception as exc:
            return JsonResponse({'errors': [str(exc)]}, status=400)

        return JsonResponse({'userId': self.user.id})

    def change(self, body):
        if 'username' in body:
            self.user.username = body['username']

        if 'newPassword' in body:
            if not self.user.check_password(body['oldPassword']):
                raise PermissionDenied(
                    'Your old password is wrong.')
            # try:
            #     RegistrationForm().validate_password(body['newPassword'])
            # except ValidationError as exc:
            #     raise ValidationError('{"newPassword": %s}' % str(exc))

            self.user.set_password(body['newPassword'])

        # form = UserChangeForm(body, instance=self.user)
        # form.is_valid()
        self.user.full_clean()
        self.user.save()
