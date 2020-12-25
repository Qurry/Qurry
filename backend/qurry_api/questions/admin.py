from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline

from .models import Question, Answer, Tag, Comment


class CommentsInline(GenericTabularInline):
    model = Comment


class AnswersInline(admin.TabularInline):
    model = Answer


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'user', )
    readonly_fields = ('id', )
    filter_horizontal = ('tags', 'vote_up_users', 'vote_down_users')
    inlines = (AnswersInline, CommentsInline,)


class AnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', )
    readonly_fields = ('id', )
    filter_horizontal = ('vote_up_users', 'vote_down_users')
    inlines = (CommentsInline,)


admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(Tag)
admin.site.register(Comment)
