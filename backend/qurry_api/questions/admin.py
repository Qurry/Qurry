from django.contrib import admin

from .models import Question, Answer, Tag

class QuestionAdmin(admin.ModelAdmin):
    filter_horizontal = ('tags',)

admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer)
admin.site.register(Tag)
