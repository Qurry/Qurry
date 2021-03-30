import json

from django.urls.base import reverse_lazy
from qurry_api.tests import ADMIN, AuthenticatedTestCase

from questions.models import Question, Tag


class QuestionsTestCase(AuthenticatedTestCase):

    random_question = Question.objects.order_by('?')[0]
    not_owned_question = Question.objects.exclude(user=ADMIN).order_by('?')[0]

    def test_permissions(self):
        response = self.request('GET', reverse_lazy('view-questions'))
        self.assertEqual(response.status_code, 401)

        response = self.request('POST', reverse_lazy('view-questions'), {
                                'title': 'test',
                                'body': 'test',
                                'tagIds': [],
                                'imageIds': [],
                                'documentIds': []}, json=True)

        self.assertEqual(response.status_code, 401)

        response = self.request('PATCH', reverse_lazy(
            'view-question-details', args=[self.random_question.id]), {'title': 'test'}, json=True)
        self.assertEqual(response.status_code, 401)

        response = self.request('DELETE', reverse_lazy(
            'view-question-details', args=[self.random_question.id]))
        self.assertEqual(response.status_code, 401)

        response = self.request('PATCH', reverse_lazy(
            'view-question-details', args=[self.not_owned_question.id]), {'title': 'test'}, json=True, authenticated=True)
        self.assertEqual(response.status_code, 403)

        response = self.request('DELETE', reverse_lazy(
            'view-question-details', args=[self.not_owned_question.id]), authenticated=True)
        self.assertEqual(response.status_code, 403)

    def test_values(self):
        response = self.request('GET', reverse_lazy(
            'view-question-details', args=[self.random_question.id]), authenticated=True)
        # TODO delete me
        self.maxDiff = None
        self.assertEqual(json.loads(response.content),
                         self.random_question.as_detailed(ADMIN))

    def test_pagination(self):
        response1 = self.request('GET', '%s?limit=4&offset=0' % reverse_lazy(
            'view-questions'), authenticated=True)
        response2 = self.request('GET', '%s?limit=4&offset=1' % reverse_lazy(
            'view-questions'), authenticated=True)
        self.assertNotEqual(response1.content, response2.content)
        self.assertEqual(len(json.loads(response1.content)), 4)

    def test_search(self):
        response = self.request('GET', '%s?search=python' % reverse_lazy(
            'view-questions'), authenticated=True)
        questions_got = list(
            question for question in json.loads(response.content))

        self.assertEqual(len(questions_got), 2)

    def test_filter(self):
        # tag_ids = list(Tag.objects.filter(
        #     name__in=['ti1', 'mensa']).values_list('id', flat=True))
        # print(tag_ids)
        # response = self.request('GET', '%s?tags=%s' % (reverse_lazy(
        #     'view-questions'), list.join(tag_ids, ',')), authenticated=True)
        # questions_got = list(
        #     question for question in json.loads(response.content))

        # self.assertEqual(len(questions_got), 2)
        pass
