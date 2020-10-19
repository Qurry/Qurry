from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode 
from django.contrib.sites.shortcuts import get_current_site
# from accounts.utilities import account_activation_token


from .models import User
from .forms import UserCreationForm

@csrf_exempt
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            '''email = form.cleaned_data.get('email')
            current_site = get_current_site(request)
            mail_subject = 'Activate your account.'
            message = render_to_string('email_template.html', {
                        'user': user,
                        'domain': current_site.domain,
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        # 'token': account_activation_token.make_token(user),
                    })
            to_email = form.cleaned_data.get('email')
            send_mail(mail_subject, message, 'youremail', [to_email])'''

            return JsonResponse({}, status=201)
        else:
            response_json = {'errors': {}}
            for field, errors in form.errors.items():
                response_json['errors'][field] = ' '.join(errors)

            return JsonResponse(response_json, status=409)

    return JsonResponse({'message': 'request is not post'}, status=400)

'''def activate(request, uidb64, token):

    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')'''

