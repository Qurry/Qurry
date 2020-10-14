from django.http import JsonResponse
from users.models import User

def testView(request):
    user = User.objects.all()[0]
    return JsonResponse({'date': user.date_joined})
