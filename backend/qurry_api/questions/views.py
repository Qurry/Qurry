import json

from django.http import JsonResponse
from django.views import View
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError, PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Question, Tag

# remove us
from users.models import User
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

def to_json(post_body):
    body_unicode = post_body.decode('utf-8')
    return json.loads(body_unicode or '{}')

def login_required(func):
    def is_authenticated(self, request, *args, **kwargs):
        print(request.user)
        if not request.user.is_authenticated:
            return JsonResponse({'not authenticated': 'you have to login to access questions'}, status=401)

        self.user = request.user
        return func(self, request, *args, **kwargs)
    return is_authenticated

""" def is_owner_of(func):
    def has_perm(self, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'not authenticated': 'you have to login to access questions'}, status=401)
        return self.func(*args, **kwargs)
    return is_authenticated """

""" def to_string(error_dict):
    error_string = ''
    for field in error_dict:
        error_string += ' %s(' % field
        for message in error_dict[field]:
            error_string += '%s, ' % message
        error_string += ') '
    return error_string """

@method_decorator(csrf_exempt, name='dispatch')
class QuestionView(View, LoginRequiredMixin):

    # different HTTP requests
    @login_required
    def get(self, request, *args, **kwargs):
        if 'id' in kwargs:
            return self.view_details(kwargs['id'])
        return self.view_list()
    
    @login_required
    def post(self, request, *args, **kwargs):
        self.user = request.user
        return self.create(to_json(request.body))

    @login_required
    def patch(self, request, *args, **kwargs):
        self.user = request.user
        if not 'id' in kwargs:
            return JsonResponse({'methode not allowed': 'you can not patch to questions, you have to add id to the url'}, status=405)
        return self.change(kwargs['id'], to_json(request.body))

    @login_required
    def delete(self, request, *args, **kwargs):
        self.user = request.user
        if not 'id' in kwargs:
            return JsonResponse({'methode not acceptable': 'you can not delete to questions, you have to add id to the url'}, status=405)
        return self.remove(kwargs['id'])

    # TODO add limit + offset
    def view_list(self): # in preview format
        return JsonResponse(list(question.as_preview() for question in Question.objects.all()), safe=False)
    
    def view_details(self, id):
        try:
            response = get_object_or_404(Question, id=id).as_detailed()
            return JsonResponse(response)
        except Exception as exception:
            error_message = self.handle(exception)
            return JsonResponse({'not found': error_message}, status=404)
     
    # TODO add login_required
    def create(self, body):
        try:
            tagIds = body['tagIds']
            tags = self.tags_from(tagIds)

            creation_data = {'title': body['title'], 'body': body['body'], 'user': self.user}

            new_question = Question(**creation_data)
            new_question.full_clean()
            new_question.save()
            new_question.tags.set(tags)
        
        except Exception as exception:
            error_message = self.handle(exception)
            return JsonResponse({'bad request': error_message}, status=400)
 
        return JsonResponse({'created': new_question.id}, status=201)

    # TODO add login_required and permission_required
    def change(self, id, body):
        try:
            question = Question.objects.get(id=id)

            if not self.user.is_owner_of(question):
                raise PermissionDenied

            if 'title' in body:
                question.title = body['title']
            if 'body' in body:
                question.body = body['body']
            
            question.full_clean()
            question.save()

            if 'tagIds' in body:
                tagIds = body['tagIds']
                tags = self.tags_from(tagIds)
                question.tags.set(tags)

        except Question.DoesNotExist as err:
            return JsonResponse({'not found': str(err)}, status=404)

        except PermissionDenied as err:
            return JsonResponse({'unautherized': 'you have to own the object to be able to change it'}, status=401)

        except Exception as exception:
            error_message = self.handle(exception)
            return JsonResponse({'bad request': error_message}, status=400)

        return JsonResponse({'changed': id}, status=201)

    # TODO add login_required and permission_required
    def remove(self, id):
        try:
            question = Question.objects.get(id=id)

            if not self.user.is_owner_of(question):
                raise PermissionDenied

            question.delete()

        except Question.DoesNotExist as err:
            return JsonResponse({'not found': str(err)}, status=404)

        except PermissionDenied as err:
            return JsonResponse({'unautherized': 'you have to own the object to be able to change it'}, status=401)

        except Exception as exception:
            error_message = self.handle(exception)
            return JsonResponse({'bad request': error_message}, status=400)

        return JsonResponse({'deleted': id}, status=200)
    
    # aux functions

    def tags_from(self, tag_ids):
        tags = []
        for tag_id in tag_ids:
            tags.append(Tag.objects.get(id=tag_id))
        return tags

    def handle(self, bad_request_exception): 
        # fields are not valid 
        if isinstance(bad_request_exception, ValidationError):
            return eval(str(bad_request_exception))

        message_dict = {
            # one argument is not given
            KeyError: 'request must contain title, body and tagIds, even it is blank.',
            # tagIds is not a list
            TypeError: 'tagIds should be a list of strings.',
        }
        return message_dict.get(type(bad_request_exception), str(bad_request_exception))
