from django.http import JsonResponse

def testView(request):
    return JsonResponse({'questions':[
        {
            'id': 1,
            'title': 'zu späte Abgabe',
            'body': 'Was passiert wenn ich meine Übung zu spät abgebe?'
        },
        {
            'id': 2,
            'title': 'Belegung Mathe III',
            'body': 'Ist Mathe III pflicht?'
        },
    ]})
