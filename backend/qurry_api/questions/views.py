import json

from django.http import JsonResponse
from django.views import View
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError, PermissionDenied, RequestAborted
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Question, Tag, Answer, Comment

# remove us
from users.models import User
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


def json_from(post_body):
    body_unicode = post_body.decode('utf-8')
    return json.loads(body_unicode or '{}')


def tags_from(tag_ids):
    tags = []
    for tag_id in tag_ids:
        tags.append(Tag.objects.get(id=int(tag_id)))
    return tags


def extract_errors(validation_exception):
    error_list = []
    error_dict = eval(str(validation_exception))
    for field in error_dict:
        for error in error_dict[field]:
            error_list.append('%s: %s' % (field, error))
    return error_list


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
            return JsonResponse({'errors': ['you have to own the %s object to be able to do this action' % self.Model.__name__]}, status=401)
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
class AbstractView(View):
    Model = None

    def setup(self, request, *args, **kwargs):
        self.user = request.user
        return super().setup(request, *args, **kwargs)

    # different HTTP requests
    @login_required
    @object_existence_required
    def get(self, request, *args, **kwargs):
        if 'id' in kwargs:
            obj = self.Model.objects.get(id=kwargs['id'])
            if 'vote' in request.GET:
                return self.vote(obj, request.GET['vote'])

            return self.view_detailed(obj)

        return self.view_list(**(request.GET.dict() | kwargs))

    @login_required
    def post(self, request, *args, **kwargs):
        try:
            return self.create(json_from(request.body))
        except ValidationError as exc:
            return JsonResponse({'errors': extract_errors(exc)}, status=400)
        except Exception as exc:
            return JsonResponse({'errors': self.handle(exc)}, status=400)

    @login_required
    @object_existence_required
    def patch(self, request, *args, **kwargs):
        if not 'id' in kwargs:
            return JsonResponse({'errors': ['you can not patch to %ss, you have to add id to the url' % self.Model.__name__]}, status=405)
        obj = self.Model.objects.get(id=kwargs['id'])
        try:
            return self.change(obj, json_from(request.body))
        except ValidationError as exc:
            return JsonResponse({'errors': extract_errors(exc)}, status=400)
        except Exception as exc:
            return JsonResponse({'errors': self.handle(exc)}, status=400)

    @login_required
    @object_existence_required
    def delete(self, request, *args, **kwargs):
        if not 'id' in kwargs:
            return JsonResponse({'errors': ['you can not delete to %ss, you have to add id to the url' % self.Model.__name__]}, status=405)
        obj = self.Model.objects.get(id=kwargs['id'])
        try:
            return self.remove(obj)
        except Exception as exc:
            return JsonResponse({'errors': [str(exc)]}, status=500)

    def view_list(self, **kwargs):  # in preview format
        pass

    def view_detailed(self, question):
        pass

    def create(self, body):
        pass

    def change(self, question, body):
        pass

    def remove(self, question):
        pass

    def vote(self, obj, action):
        # remove user from voters
        try:
            obj.vote_up_users.remove(self.user)
        except:
            pass

        try:
            obj.vote_down_users.remove(self.user)
        except:
            pass

        if action == '1':
            obj.vote_up_users.add(self.user)
        if action == '-1':
            obj.vote_down_users.add(self.user)

        return JsonResponse({'%sId' % self.Model.__name__.lower(): str(obj.id)})


class QuestionView(AbstractView):

    Model = Question

    def view_list(self, **kwargs):  # in preview format
        # parse arguments
        limit = Question.objects.count()
        offset = 0
        search_words = None
        try:
            if 'limit' in kwargs:
                limit = int(kwargs['limit'])

            if 'offset' in kwargs:
                offset = int(kwargs['offset'])

            if 'search' in kwargs:
                search_words = kwargs['search'].split(' ')
        except:
            return JsonResponse({'errors': ['get arguments are invalid']}, status=400)

        # print(search_words, kwargs['search']) throws error if no search parameter

        questions = Question.objects.all()

        search_result = Question.objects.none()
        if search_words:
            for word in search_words:
                search_result |= questions.filter(title__icontains=word)
                search_result |= questions.filter(body__icontains=word)

            questions = search_result

        return JsonResponse(list(question.as_preview() | {'userVote': question.vote_of(self.user)} for question in questions[offset: offset + limit]), safe=False)

    def view_detailed(self, question):
        return JsonResponse(question.as_detailed() | {'userVote': question.vote_of(self.user)})

    def create(self, body):
        tagIds = body['tagIds']
        tags = tags_from(tagIds)

        creation_data = {'title': body['title'],
                         'body': body['body'], 'user': self.user}

        new_question = Question(**creation_data)
        new_question.full_clean()
        new_question.save()
        new_question.tags.set(tags)

        return JsonResponse({'questionId': str(new_question.id)}, status=201)

    @ownership_required
    def change(self, question, body):
        if 'title' in body:
            question.title = body['title']
        if 'body' in body:
            question.body = body['body']

        question.full_clean()
        question.save()

        if 'tagIds' in body:
            tagIds = body['tagIds']
            tags = tags_from(tagIds)
            question.tags.set(tags)

        return JsonResponse({'questionId': str(question.id)}, status=200)

    @ownership_required
    def remove(self, question):
        question.delete()

        return JsonResponse({'questionId': str(question.id)}, status=200)

    def handle(self, bad_request_exception):
        # fields are not valid
        message_dict = {
            # one argument is not given
            KeyError: 'request must contain title, body and tagIds, even it is blank.',
            # tagIds is not a list
            TypeError: 'tagIds should be a list of strings.',
        }
        return [message_dict.get(type(bad_request_exception), str(bad_request_exception))]


class TagView(View):
    # @login_required throws AttributeError at /api/tags/ 'TagView' object has no attribute 'user'
    def get(self, request, *args, **kwargs):
        return self.view_list()

    def view_list(self):
        return JsonResponse(list(tag.as_preview() for tag in Tag.objects.all()), safe=False)


class AnswerView(AbstractView):
    Model = Answer
    question = None

    def setup(self, request, *args, **kwargs):
        if 'qid' in kwargs:
            try:
                self.question = Question.objects.get(id=kwargs['qid'])
            except:
                pass
        return super().setup(request, *args, **kwargs)

    def view_list(self, **kwargs):  # in preview format
        if self.question:
            return JsonResponse(list(answer.as_preview() | {'userVote': answer.vote_of(self.user)} for answer in self.question.answer_set.all()), safe=False)
        return JsonResponse(
            list(answer.as_preview() | {'userVote': answer.vote_of(self.user), 'questionId': str(answer.question_id)}
                 for answer in Answer.objects.all()),
            safe=False)

    def view_detailed(self, answer):
        return JsonResponse(answer.as_preview() | {'userVote': answer.vote_of(self.user), 'questionId': str(answer.question_id)})

    def create(self, body):

        if not self.question:
            raise RequestAborted(
                'you can create an answer with questions/<id>/answers/')

        creation_data = {
            'body': body['body'], 'user': self.user, 'question': self.question}

        new_answer = Answer(**creation_data)
        new_answer.full_clean()
        new_answer.save()

        return JsonResponse({'answerId': str(new_answer.id)}, status=201)

    @ownership_required
    def change(self, answer, body):

        if 'body' in body:
            answer.body = body['body']

        answer.full_clean()
        answer.save()

        return JsonResponse({'answerId': str(answer.id)}, status=200)

    @ownership_required
    def remove(self, answer):
        answer.delete()

        return JsonResponse({'answerId': str(answer.id)}, status=200)

    def handle(self, bad_request_exception):
        # fields are not vali

        message_dict = {
            # one argument is not given
            KeyError: 'request must contain body',
        }
        return [message_dict.get(type(bad_request_exception), str(bad_request_exception))]


class CommentView(AbstractView):
    Model = Comment
    question = None
    answer = None

    def setup(self, request, *args, **kwargs):
        if 'qid' in kwargs:
            try:
                self.question = Question.objects.get(id=kwargs['qid'])
            except:
                pass
        if 'aid' in kwargs:
            try:
                self.answer = Answer.objects.get(id=kwargs['aid'])
            except:
                pass
        return super().setup(request, *args, **kwargs)

    def view_list(self, **kwargs):  # in preview format
        if self.answer:
            return JsonResponse(list(comment.as_preview() for comment in self.answer.comments.all()), safe=False)
        if self.question:
            return JsonResponse(list(comment.as_preview() for comment in self.question.comments.all()), safe=False)
        return JsonResponse(list(comment.as_preview() for comment in Comment.objects.all()), safe=False)

    def view_detailed(self, comment):
        return JsonResponse(comment.as_preview())

    def create(self, body):

        if not self.question and not self.answer:
            raise RequestAborted(
                'you can create a comment with questions/<id>/comments/ or answers/<id>/comments')

        if self.answer:
            creation_data = {
                'body': body['body'], 'user': self.user, 'content_object': self.answer}
        else:
            creation_data = {
                'body': body['body'], 'user': self.user, 'content_object': self.question}

        new_comment = Comment(**creation_data)
        new_comment.full_clean()
        new_comment.save()

        return JsonResponse({'commentId': str(new_comment.id)}, status=201)

    @ ownership_required
    def change(self, comment, body):

        if 'body' in body:
            comment.body = body['body']

        comment.full_clean()
        comment.save()

        return JsonResponse({'commentId': str(comment.id)}, status=200)

    @ ownership_required
    def remove(self, comment):
        comment.delete()

        return JsonResponse({'commentId': str(comment.id)}, status=200)

    def vote(self, answer, action):
        return JsonResponse({'error': ['you can not vote comments now']}, status=405)

    def handle(self, bad_request_exception):
        # fields are not vali

        message_dict = {
            # one argument is not given
            KeyError: 'request must contain body',
        }
        return [message_dict.get(type(bad_request_exception), str(bad_request_exception))]
