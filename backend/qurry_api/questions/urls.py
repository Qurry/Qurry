from django.urls import path, include
from django.http import JsonResponse

from .views import QuestionView

def mockquestions(request):
    return JsonResponse(
        [
            {
                "id": 3,
                "title": "Was ist die Lösung für die Matheaufgabe 3.4a?",
                "body": "It is a long established fact that a reader will be distracted by the readable content of a page when looking at its layout. The point of using Lorem Ipsum is that it has a more-or-less normal distribution of letters, as opposed to using 'Content here, content here', making it look like readable English. Many desktop publishing packages and web page editors now use Lorem Ipsum as their default model text, and a search for 'lorem ipsum' will uncover many web sites still in their infancy. Various versions have evolved over the years, sometimes by accident, sometimes on purpose (injected humour and the like).",
                "votes": 0,
                "dateTime": "2020-11-02T20:27:52.417252Z",
                "tags": [{
                    "id": 3,
                    "name": "ma3",
                    "description": "Mathematik 3"
                }],
                "answers": 0,
                "user": {
                    "id": 1,
                    "username": "tom"
                }
            },
            {
                "id": 4,
                "title": "Was ist der Unterschied zwischen der Borelalgebra und Borelmengen?",
                "body": "It is a long established fact that a reader will be distracted by the readable content of a page when looking at its layout. The point of using Lorem Ipsum is that it has a more-or-less normal distribution of letters, as opposed to using 'Content here, content here', making it look like readable English. Many desktop publishing packages and web page editors now use Lorem Ipsum as their default model text, and a search for 'lorem ipsum' will uncover many web sites still in their infancy. Various versions have evolved over the years, sometimes by accident, sometimes on purpose (injected humour and the like).",
                "votes": 3,
                "dateTime": "2020-11-30T20:27:52.417252Z",
                "tags": [{
                    "id": 3,
                    "name": "ma3",
                    "description": "Mathematik 3"
                }],
                "answers": 1,
                "user": {
                    "id": 2,
                    "username": "abdu"
                }
            },
            {
                "id": 5,
                "title": "Müssen wir in der Klausur ableiten können?",
                "body": "Meine Schulzeit liegt schon länger zurück und ich kann nicht mehr richtig ableiten. Muss ich das für die Klausur lernen?",
                "votes": -2,
                "dateTime": "2020-12-08T21:23:34.417252Z",
                "tags": [{
                    "id": 3,
                    "name": "ma3",
                    "description": "Mathematik 3"
                }],
                "answers": 3,
                "user": {
                    "id": 1,
                    "username": "tom"
                }
            }
        ],
        safe = False
    )

urlpatterns = [
    # path('questions/', mockquestions),
    path('questions', QuestionView.as_view(), name='view-questions'),
    path('questions/<int:id>', QuestionView.as_view(), name='view-question-details'),
]
