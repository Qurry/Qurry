from django.contrib import admin
from django.contrib.contenttypes import fields
from django.contrib.contenttypes.admin import GenericTabularInline

from .models import Question, Answer, Tag, Comment, TagCategory


class CommentsInline(GenericTabularInline):
    model = Comment


class AnswersInline(admin.TabularInline):
    model = Answer


class TagsInline(admin.TabularInline):
    model = Tag


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'user',)
    readonly_fields = ('id',)
    filter_horizontal = ('tags', 'vote_up_users', 'vote_down_users')
    inlines = (AnswersInline, CommentsInline,)


class AnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'user',)
    readonly_fields = ('id',)
    filter_horizontal = ('vote_up_users', 'vote_down_users')
    inlines = (CommentsInline,)


class TagAdmin(admin.ModelAdmin):
    inlines = (TagsInline,)


admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(TagCategory, TagAdmin)
admin.site.register(Comment)
