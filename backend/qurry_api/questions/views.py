from django.shortcuts import render
from django.http import JsonResponse

from .models import Question, Answer, Tag
from users.models import User

def get_user(uid):
    user = User.objects.filter(id=uid)[0]
    return {
            'id': uid,
            'name': user.name,
            'score': user.score,
        }

def get_tags(qid):
    return [{'id': tag.id, 'name': tag.name} for tag in Question.objects.filter(id=qid)[0].tags.all() ]

def get_answers(qid):

    answers = Answer.objects.filter(question__id=qid).all()
    answerlist = []

    for answer in answers:
        answerlist.append({
            'id': answer.id,
            'body': answer.body,
            'dateTime': answer.date_time,
            'votes': answer.votes,
            'user': get_user(answer.user.id),
        })

    return answerlist

def return_questions(request):

    questions = Question.objects.all()
    json = []

    if not request.GET:
        for question in questions:
                        
            json.append({
                'id': question.id,
                'title': question.title,
                'votes': question.votes,
                'dateTime': question.date_time,
                'user': get_user(question.user.id),
                'answers': len(Answer.objects.filter(question__id=question.id)),
                'tags': get_tags(question.id),
            })

        return JsonResponse(json, safe=False)

def view_question(request, qid):
    question = Question.objects.filter(id=qid)[0]
    answers = []

    return JsonResponse({
                'id': question.id,
                'title': question.title,
                'body': question.body,
                'votes': question.votes,
                'dateTime': question.date_time,
                'user': get_user(question.id),
                'answers': get_answers(question.id),
                'tags': get_tags(question.id),
            }, safe=False)
