import json
from django.http.response import JsonResponse

from qurry_api.base_views import AuthenticatedView
from qurry_api.decorators import object_existence_required


class FileView(AuthenticatedView):
    Model = None

    @object_existence_required
    def get(self, request, *args, **kwargs):
        if 'id' in kwargs:
            file = self.Model.objects.get(id=kwargs['id'])
            return self.response_with(file)
        else:
            return JsonResponse({'errors': ['you can either add a new file or get a specific file']}, status=405)

    def post(self, request, *args, **kwargs):
        file = request.FILES['file']
        try:
            file_obj = self.create(file, description=request.POST.get('description'))
        except Exception as exc:
            return JsonResponse({'errors': [str(exc)]}, status=400)

        return JsonResponse(file_obj.as_preview())

    def create(self, file, **kwargs):
        file_object = self.Model(src=file, user=self.user, description=kwargs.get('description'))
        file_object.full_clean()
        file_object.save()

        return file_object
    
    # TODO def change(self, file, **kwargs):
    #     if

    # TODO def remove

    def response_with(self, file):
        return JsonResponse({'%sUrl' % self.Model.__name__.lower(): file.src.url})
