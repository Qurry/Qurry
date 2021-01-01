import secrets
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from questions.views import json_from, extract_errors
from qurry_api import settings
from qurry_api.base_views import AthenticatedView
from qurry_api.decorators import login_required

from .forms import UserCreationForm
from .models import User, Token


def active_user_exists(function):
    def does_active_exist(self, *args, **kwargs):
        if 'id' in kwargs:
            try:
                User.objects.get(id=kwargs['id'], is_active=True)
            except Exception as err:
                return JsonResponse({'errors': [str(err)]}, status=404)
        return function(self, *args, **kwargs)

    return does_active_exist


def make_token(user):
    token = secrets.token_urlsafe(30)
    Token(user=user, token=token).save()
    return token


def is_valid(user, token):
    exists = Token.objects.filter(user=user.id).filter(token=token)
    if len(exists) == 1:
        exists[0].delete()
        return True
    else:
        return False


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            token = make_token(user)
            mail_subject = 'Activate your account.'
            current_site = get_current_site(request)
            message = render_to_string('email_template.html', {
                'user': user,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': token,
                'domain': current_site.domain,
            })
            to_email = form.cleaned_data.get('email')
            send_mail(mail_subject, message,
                      settings.EMAIL_HOST_USER, [to_email])

            return JsonResponse({}, status=201)
        else:
            response_json = {'errors': {}}
            for field, errors in form.errors.items():
                response_json['errors'][field] = ' '.join(errors)

            return JsonResponse(response_json, status=409)

    return JsonResponse({'message': 'request is not post'}, status=400)


def activate(request, uidb, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and is_valid(user, token):
        user.is_active = True
        user.save()

        # create profile for user
        user.get_default_profile()

        return HttpResponse(
            'Thank you for your email confirmation. Now you can <a href="localhost:3000/login">login</a> your account.')
    else:
        return HttpResponse('Activation link is invalid!')


class UserView(AthenticatedView):
    Model = User
    mode = None

    @login_required
    @active_user_exists
    def get(self, *_, **kwargs):
        if self.mode == 'profile':
            return self.profile()

        if 'id' in kwargs:
            user = User.objects.get(id=kwargs['id'])
            return JsonResponse(user.as_detailed())

        return JsonResponse(list(user.as_detailed() for user in User.objects.all_active()), safe=False)

    @login_required
    def patch(self, *_, **__):
        if self.mode != 'profile':
            return JsonResponse({'errors': ['if you need to edit your profile, PATCH to profile/']}, status=405)
        try:
            self.change(**json_from(request.body))
        except ValidationError as exc:
            return JsonResponse({'errors': extract_errors(exc)}, status=400)
        except Exception as exc:
            return JsonResponse({'errors': [str(exc)]}, status=400)

        return JsonResponse({'userId': self.user.id})

    def profile(self):
        return JsonResponse(self.user.as_detailed() | {
            'email': self.user.email,
            'registeredAt': timezone.localtime(self.user.registered_at)
        })

    def change(self, **kwargs):
        if 'username' in kwargs:
            self.user.username = kwargs['username']

        if 'password' in kwargs:
            self.user.set_password(kwargs['password'])

        self.user.full_clean()
        self.user.save()
