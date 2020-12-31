from django.http.response import JsonResponse

from qurry_api.base_views import AthenticatedView
from qurry_api.decorators import login_required, object_existence_required


def response(file):
        
    print(file.src.url)
    return JsonResponse({})


class FileView(AthenticatedView):
    Model = None

    @ object_existence_required
    def get(self, request, *args, **kwargs):
        if 'id' in kwargs:
            file = self.Model.objects.get(id=kwargs['id'])
            return response(file)
        else:
            return JsonResponse({'errors': ['you can either add a new file or get a spesific file']}, status=405)

    # @ login_required
    def post(self, request, *args, **kwargs):
        print(request.FILES)
        return JsonResponse({str(request.FILES)}, safe=False)