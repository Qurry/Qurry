from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from mptt.admin import DraggableMPTTAdmin, TreeRelatedFieldListFilter

from .models import Answer, Comment, Question, Tag


class CommentsInline(GenericTabularInline):
    model = Comment


class AnswersInline(admin.TabularInline):
    model = Answer


class TagsInline(admin.TabularInline):
    model = Tag


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at')
    readonly_fields = ('id',)
    filter_horizontal = ('tags', 'vote_up_users', 'vote_down_users')
    list_filter = (('tags', TreeRelatedFieldListFilter), 'created_at')
    inlines = (AnswersInline, CommentsInline,)


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at')
    readonly_fields = ('id',)
    filter_horizontal = ('vote_up_users', 'vote_down_users')
    list_filter = ('created_at',)
    inlines = (CommentsInline,)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)
    list_display = ('id', 'user', 'created_at')


@admin.register(Tag)
class TagAdmin(DraggableMPTTAdmin):
    list_display = ('tree_actions', 'indented_title', 'id')
