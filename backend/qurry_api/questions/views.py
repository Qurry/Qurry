from abc import abstractmethod

from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django.http import JsonResponse
from qurry_api.decorators import object_existence_required, ownership_required
from qurry_api.views import BaseView, error_list_from

from questions.forms import (AnswerActionForm, AnswerForm, CommentForm,
                             QuestionActionForm, QuestionForm)

from .models import Answer, Comment, Question, Tag

DEFAULT_LIMIT = 10
DEFAULT_ERROR_MESSAGE = 'error while parsing input'
DEFAULT_ORDER_BY = 'votes'


def extract_errors(validation_exception):
    error_list = []
    error_dict = eval(str(validation_exception))
    if isinstance(error_dict, list):
        error_dict = eval(error_dict[0])
    for field in error_dict:
        for error in error_dict[field]:
            error_list.append('%s: %s' % (field, error))
    return error_list


class AbstractView(BaseView):
    Model = None
    Form = None
    ActionForm = None

    # different HTTP requests
    @object_existence_required
    def get(self, request, *args, **kwargs):
        # return one object
        if 'id' in kwargs:
            obj = self.Model.objects.get(id=kwargs['id'])
            if request.GET and self.ActionForm:
                form = self.ActionForm(request.GET.dict(), obj, self.user)
                if form.is_valid():
                    form.save()
                else:
                    return JsonResponse({'errors': error_list_from(form.errors)}, status=400)
            return self.view_detailed(obj)

        # return all objects
        try:
            return self.view_list(**({**request.GET.dict(), **kwargs}))
        except Exception:
            return JsonResponse({'errors': ['get arguments are invalid']}, status=400)

    def post(self, request, *args, **kwargs):
        form = self.Form(self.form_data({**request.body, **kwargs}))
        if form.is_valid():
            instance = form.save()
            return JsonResponse({f'{self.Model.__name__.lower()}Id': str(instance.id)}, status=201)

        return JsonResponse({'errors': error_list_from(form.errors)}, status=400)

    @ object_existence_required
    @ ownership_required
    def patch(self, request, *args, **kwargs):
        if 'id' not in kwargs:
            return JsonResponse(
                {'errors': [
                    'you can not patch to %ss, you have to add id to the url' % self.Model.__name__]},
                status=405)

        instance = self.Model.objects.get(id=kwargs['id'])
        form = self.Form(self.form_data(
            {**request.body, **kwargs}), instance=instance)
        if form.is_valid():
            instance = form.save()
            return JsonResponse({f'{self.Model.__name__.lower()}Id': str(instance.id)}, status=200)

        return JsonResponse({'errors': error_list_from(form.errors)}, status=400)

    @ object_existence_required
    @ ownership_required
    def delete(self, request, *args, **kwargs):
        if 'id' not in kwargs:
            return JsonResponse(
                {'errors': [
                    'you can not delete to %ss, you have to add id to the url' % self.Model.__name__]},
                status=405)
        instance = self.Model.objects.get(id=kwargs['id'])
        try:
            instance.delete()
            return JsonResponse({'%sId' % self.Model.__name__.lower(): str(kwargs['id'])}, status=200)
        except Exception as exc:
            return JsonResponse({'errors': [str(exc)]}, status=500)

    @ abstractmethod
    def view_list(self, **kwargs):  # in preview format
        pass

    @ abstractmethod
    def view_detailed(self, obj):
        pass

    @ abstractmethod
    def form_data(self, raw_data):
        pass


class QuestionView(AbstractView):
    Model = Question
    Form = QuestionForm
    ActionForm = QuestionActionForm

    def view_list(self, **kwargs):  # in preview format
        # parse arguments
        limit = abs(int(kwargs.get('limit', DEFAULT_LIMIT)))
        offset = abs(int(kwargs.get('offset', 0)))

        search_vector = kwargs.get('words', '').split()

        tag_ids = kwargs.get('tags', '')
        filter_tags = Tag.objects.none()
        if tag_ids != '':
            filter_tags = Tag.objects.filter(id__in=list(
                int(id) for id in tag_ids.split(',')))

        order_by = kwargs.get('order_by', DEFAULT_ORDER_BY)

        # collect queries for database
        queries = []
        # user_id = kwargs.get('user')
        # if user_id:
        #     queries.append(Q(user__id=user_id))

        answered = kwargs.get('answered', None)
        if answered == 'false':
            queries.append(Q(answer_count=0))
        elif answered == 'true':
            queries.append(~Q(answer_count=0))

        questions = Question.objects.filter(*queries).tag_filter(filter_tags).search(
            search_vector).order_by(order_by)[offset: offset+limit]

        return JsonResponse({
            'count': questions.count(),
            'questions': list(question.as_preview(self.user) for question in questions)
        })

    def view_detailed(self, question):
        return JsonResponse(question.as_detailed(self.user))

    def form_data(self, raw_data):
        raw_data['tags'] = raw_data.get('tagIds', [])
        raw_data['images'] = raw_data.get('imageIds', [])
        raw_data['documents'] = raw_data.get('documentIds', [])

        return {**raw_data, 'user': self.user}


class AnswerView(AbstractView):
    Model = Answer
    Form = AnswerForm
    ActionForm = AnswerActionForm
    question = None

    def setup(self, request, *args, **kwargs):
        # TODO: refactor question parsing
        if 'qid' in kwargs:
            try:
                self.question = Question.objects.get(id=kwargs['qid'])
            except:
                pass
        return super().setup(request, *args, **kwargs)

    def view_list(self, **kwargs):  # in preview format
        if self.question:
            return JsonResponse(list(answer.as_preview(self.user) for answer in self.question.answer_set.all()),
                                safe=False)
        return JsonResponse(list(answer.as_preview(self.user) for answer in Answer.objects.all()), safe=False)

    def view_detailed(self, answer):
        return JsonResponse(answer.as_detailed(self.user))

    def form_data(self, raw_data):
        raw_data['question'] = self.question
        raw_data['images'] = raw_data.get('imageIds', [])
        raw_data['documents'] = raw_data.get('documentIds', [])

        return {**raw_data, 'user': self.user}


class CommentView(AbstractView):
    Model = Comment
    Form = CommentForm
    commented_object = None

    def setup(self, request, *args, **kwargs):
        # TODO: refactor commented object parsing
        if 'qid' in kwargs:
            try:
                self.commented_object = Question.objects.get(id=kwargs['qid'])
            except:
                pass
        if 'aid' in kwargs:
            try:
                self.commented_object = Answer.objects.get(id=kwargs['aid'])
            except:
                pass
        return super().setup(request, *args, **kwargs)

    def view_list(self, **kwargs):  # in preview format
        if self.commented_object:
            return JsonResponse(list(comment.as_preview() for comment in self.commented_object.comments.all()), safe=False)
        return JsonResponse(list(comment.as_preview() for comment in Comment.objects.all()), safe=False)

    def view_detailed(self, comment):
        return JsonResponse(comment.as_detailed())

    def form_data(self, raw_data):
        return {
            **raw_data,
            'user': self.user,
            **self.commented_object_data(raw_data)
        }

    def commented_object_data(self, raw_data):
        if 'qid' in raw_data:
            return {
                'object_id': raw_data['qid'],
                'content_type': ContentType.objects.get(model='question')
            }

        if 'aid' in raw_data:
            return {
                'object_id': raw_data['aid'],
                'content_type': ContentType.objects.get(model='answer')
            }

        return {}


class TagView(BaseView):

    def get(self, request, *args, **kwargs):
        return self.view_list()

    def view_list(self):
        return JsonResponse(Tag.all_as_preview(), safe=False)
