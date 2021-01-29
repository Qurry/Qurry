from django.http.response import JsonResponse

from qurry_api.base import AuthenticatedView, object_existence_required, ownership_required


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
        file_data = request.FILES.get('file')
        try:
            file_obj = self.create(
                file_data, description=request.POST.get('description', ''))
        except Exception as exc:
            return JsonResponse({'errors': [str(exc)]}, status=400)

        return JsonResponse(file_obj.as_preview())

    @object_existence_required
    @ownership_required
    def patch(self, request, *args, **kwargs):
        if 'id' not in kwargs:
            return JsonResponse(
                {'errors': [
                    'you can not patch to %ss, you have to add id to the url' % self.Model.__name__]},
                status=405)
        file_obj = self.Model.objects.get(id=kwargs['id'])
        try:
            self.change(file_obj,
                        description=request.POST.get('description', ''))
        except Exception as exc:
            return JsonResponse({'errors': [str(exc)]}, status=400)

        return JsonResponse(file_obj.as_preview())

    @object_existence_required
    @ownership_required
    def delete(self, request, *args, **kwargs):
        if 'id' not in kwargs:
            return JsonResponse(
                {'errors': [
                    'you can not delete to %ss, you have to add id to the url' % self.Model.__name__]},
                status=405)
        obj = self.Model.objects.get(id=kwargs['id'])
        try:
            obj.delete()
            return JsonResponse({'%sId' % self.Model.__name__.lower(): str(kwargs['id'])}, status=200)
        except Exception as exc:
            return JsonResponse({'errors': [str(exc)]}, status=500)

    def create(self, file, **kwargs):
        file_object = self.Model(
            src=file, user=self.user, description=kwargs.get('description', ''))
        file_object.full_clean()
        file_object.save()

        return file_object

    def change(self, file_object, file_data, **kwargs):
        if kwargs.get('description'):
            file_object.description = kwargs.get('description')

        file_object.full_clean()
        file_object.save()

    def response_with(self, file):
        return JsonResponse({'%sUrl' % self.Model.__name__.lower(): file.src.url})
