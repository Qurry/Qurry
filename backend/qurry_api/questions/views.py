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

# parse a post body and return json


def json_from(post_body):
    body_unicode = post_body.decode('utf-8')
    return json.loads(body_unicode or '{}')

# decorators


def login_required(function):
    def is_authenticated(self, *args, **kwargs):
        if not self.user.is_authenticated:
            return JsonResponse({'errors': ['you have to login to access questions']}, status=401)
        return function(self, *args, **kwargs)
    return is_authenticated


def ownership_required(function):
    def is_owner(self, obj, *args, **kwargs):
        if not self.user.is_owner_of(obj):
            return JsonResponse({'errors': ['you have to own the %s object to be able to do this action' % self.model.__name__]}, status=401)
        return function(self, obj, *args, **kwargs)
    return is_owner


def object_existence_required(function):
    def does_exist(self, *args, **kwargs):
        if 'id' in kwargs:
            try:
                self.Model.objects.get(id=kwargs['id'])
            except Exception as err:
                return JsonResponse({'errors': [str(err)]}, status=404)
        return function(self, *args, **kwargs)
    return does_exist


@method_decorator(csrf_exempt, name='dispatch')
class QuestionView(View):

    Model = Question

    def setup(self, request, *args, **kwargs):
        self.user = request.user
        return super().setup(request, *args, **kwargs)

    # different HTTP requests
    @object_existence_required
    def get(self, request, *args, **kwargs):
        if 'id' in kwargs:
            question = self.Model.objects.get(id=kwargs['id'])
            if 'vote' in request.GET:
                return self.vote(question, request.GET['vote'])

            return self.view_detailed(question)

        return self.view_list(**dict(request.GET))

    def post(self, request, *args, **kwargs):
        return self.create(json_from(request.body))

    @object_existence_required
    def patch(self, request, *args, **kwargs):
        if not 'id' in kwargs:
            return JsonResponse({'errors': ['you can not patch to questions, you have to add id to the url']}, status=405)
        question = self.Model.objects.get(id=kwargs['id'])
        return self.change(question, json_from(request.body))

    @object_existence_required
    def delete(self, request, *args, **kwargs):
        if not 'id' in kwargs:
            return JsonResponse({'errors': ['you can not delete to questions, you have to add id to the url']}, status=405)
        question = self.Model.objects.get(id=kwargs['id'])
        return self.remove(question)

    @login_required
    def view_list(self, **kwargs):  # in preview format
        # parse arguments
        limit = self.Model.objects.count()
        offset = 0
        search_words = None
        try:
            if 'limit' in kwargs:
                limit = int(kwargs['limit'][0])

            if 'offset' in kwargs:
                offset = int(kwargs['offset'][0])

            if 'search' in kwargs:
                search_words = kwargs['search']
        except:
            return JsonResponse({'errors': ['get arguments are invalid']}, status=400)

        questions = self.Model.objects.all()

        search_result = Question.objects.none()
        if search_words:
            for word in search_words:
                search_result |= questions.filter(title__icontains=word)
                search_result |= questions.filter(body__icontains=word)

            questions = search_result

        return JsonResponse(list(question.as_preview() | {'userVote': question.vote_of(self.user)} for question in questions[offset: offset + limit]), safe=False)

    @login_required
    def view_detailed(self, question):
        return JsonResponse(question.as_detailed() | {'userVote': question.vote_of(self.user)})

    @login_required
    def create(self, body):
        try:
            tagIds = body['tagIds']
            tags = self.tags_from(tagIds)

            creation_data = {'title': body['title'],
                             'body': body['body'], 'user': self.user}

            new_question = self.Model(**creation_data)
            new_question.full_clean()
            new_question.save()
            new_question.tags.set(tags)

        except Exception as exception:
            error_list = self.handle(exception)
            return JsonResponse({'errors': error_list}, status=400)

        return JsonResponse({'questionId': str(new_question.id)}, status=201)

    @login_required
    @ownership_required
    def change(self, question, body):
        try:
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

        except Exception as exception:
            error_list = self.handle(exception)
            return JsonResponse({'errors': error_list}, status=400)

        return JsonResponse({'questionId': str(id)}, status=201)

    @login_required
    @ownership_required
    def remove(self, question):
        try:
            question.delete()
        except Exception as exception:
            error_list = self.handle(exception)
            return JsonResponse({'errors': error_list}, status=400)

        return JsonResponse({'questionId': str(id)}, status=200)

    @login_required
    def vote(self, question, action):
        # remove user from voters
        try:
            question.vote_up_users.remove(self.user)
        except:
            pass

        try:
            question.vote_down_users.remove(self.user)
        except:
            pass

        if action == 'up':
            question.vote_up_users.add(self.user)
        if action == 'down':
            question.vote_down_users.add(self.user)

        return JsonResponse({})

    def tags_from(self, tag_ids):
        tags = []
        for tag_id in tag_ids:
            tags.append(Tag.objects.get(id=int(tag_id)))
        return tags

    def handle(self, bad_request_exception):
        # fields are not valid
        if isinstance(bad_request_exception, ValidationError):
            error_list = []
            error_dict = eval(str(bad_request_exception))
            for field in error_dict:
                for error in error_dict[field]:
                    error_list.append('%s: %s' % (field, error))
            return error_list

        message_dict = {
            # one argument is not given
            KeyError: 'request must contain title, body and tagIds, even it is blank.',
            # tagIds is not a list
            TypeError: 'tagIds should be a list of strings.',
        }
        return [message_dict.get(type(bad_request_exception), str(bad_request_exception))]


class TagView(View):

    def get(self, request, *args, **kwargs):
        return self.view_list()

    @login_required
    def view_list(self):
        return JsonResponse(list(tag.as_preview() for tag in Tag.objects.all()), safe=False)
