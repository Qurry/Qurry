from django.http.response import JsonResponse

from qurry_api.base_views import AuthenticatedView
from qurry_api.decorators import login_required, object_existence_required


class FileView(AuthenticatedView):
    Model = None

    @login_required
    @object_existence_required
    def get(self, request, *args, **kwargs):
        if 'id' in kwargs:
            file = self.Model.objects.get(id=kwargs['id'])
            return self.response_with(file)
        else:
            return JsonResponse({'errors': ['you can either add a new file or get a specific file']}, status=405)

    @login_required
    def post(self, request, *args, **kwargs):
        file = request.FILES['file']
        try:
            file_id = self.create(file)
        except Exception as exc:
            return JsonResponse({'errors': [str(exc)]}, status=400)

        return JsonResponse({'%sId' % (self.Model.__name__.lower()): file_id})

    def create(self, file):
        file_object = self.Model(src=file, user=self.user)
        file_object.full_clean()
        file_object.save()

        return file_object.id

    def response_with(self, file):
        return JsonResponse({'data': file.src.read().hex()})
