from django.http import JsonResponse
from users.models import User

def testView(request):
    # user = User.objects.all()[0]
    # return JsonResponse({'date': user.date_joined})
    return JsonResponse( [
        {
        "id": 1,
        "title": "Tincidunt praesent semper feugiat nibh sed pulvinar proin?",
        "votes": 6,
        "answers": 2,
        "dateTime": "2020-10-14T13:50:48.187Z",
        "user": {
            "id": 23,
            "name": "Max"
        },
        "tags": [
            {
            "id": 12,
            "name": "technical"
            },
            {
            "id": 7,
            "name": "meinel"
            }
        ]
        },
        {
        "id": 2,
        "title": "Optio molestias id quia eum?",
        "votes": -2,
        "answers": 1,
        "dateTime": "2020-10-14T13:50:48.187Z",
        "user": {
            "id": 23,
            "name": "Max"
        },
        "tags": [
            {
            "id": 12,
            "name": "meinel"
            },
            {
            "id": 7,
            "name": "studienref"
            }
        ]
        },
        {
        "id": 3,
        "title": "Ea molestias quasi exercitationem repellat qui ipsa sit aut?",
        "votes": 0,
        "answers": 0,
        "dateTime": "2020-10-14T13:50:48.187Z",
        "user": {
            "id": 23,
            "name": "Max"
        },
        "tags": [
            {
            "id": 12,
            "name": "swa"
            }
        ]
        }
    ], safe=False
    )
