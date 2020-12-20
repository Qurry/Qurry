import json

from django.http import JsonResponse
from django.views import View
from django.shortcuts import get_object_or_404

from .models import Question, Tag

# remove us
from users.models import User
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

def to_json(post_body):
    body_unicode = post_body.decode('utf-8')
    return json.loads(body_unicode)

@method_decorator(csrf_exempt, name='dispatch')
class QuestionView(View):

    def get(self, request, *args, **kwargs):
        self.user = request.user
        if 'id' in kwargs:
            return self.get_details(kwargs['id'])
        return self.get_all()
    
    def post(self, request, *args, **kwargs):
        self.user = request.user
        return self.create(to_json(request.body))

    # TODO add limit + offset
    def get_all(self): # in preview format
        return JsonResponse(list(question.as_preview() for question in Question.objects.all()), safe=False)
    
    def get_details(self, id):
        response = get_object_or_404(Question, id=id).as_detailed()
        return JsonResponse(response)

    def has_valid_form(self, body):
        # check if it contains all three elements
        if set(body.keys()) != {'title', 'body', 'tagIds'}:
            return False
        return True 
     
    def parse_tags_from(self, tag_ids):
        tags = []
        for tag_id in tag_ids:
            tags.append(get_object_or_404(Tag, id=tag_id))
        return tags

    def create(self, body):
        try:
            if not self.has_valid_form(body):
                raise ValueError()
            tags = self.parse_tags_from(body['tagIds'])
            del body['tagIds']
            new_question = Question(**body)
            # when having problems use new_question.user = User.objects.first() 
            new_question.user = self.user
            new_question.save()
            new_question.tags.set(tags)
            
        except:
            return JsonResponse('bad request', status=400, safe=False)
        

        return JsonResponse('question successfully created', status=201, safe=False)
