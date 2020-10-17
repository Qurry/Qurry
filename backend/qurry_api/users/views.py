from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from .models import User
from .forms import UserCreationForm

@csrf_exempt
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({}, status=201)
        else:
            response_json = {'errors': {}}
            for field, errors in form.errors.items():
                response_json['errors'][field] = ' '.join(errors)

            return JsonResponse(response_json, status=409)

    return JsonResponse({'message': 'request is not post'}, status=400)

