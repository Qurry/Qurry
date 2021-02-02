from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from mptt.admin import DraggableMPTTAdmin, TreeRelatedFieldListFilter

from .models import Question, Answer, Tag, Comment


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
    list_filter = (('tags', TreeRelatedFieldListFilter), 'created_at')
    inlines = (AnswersInline, CommentsInline,)


class AnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'user',)
    readonly_fields = ('id',)
    filter_horizontal = ('vote_up_users', 'vote_down_users')
    list_filter = ('created_at',)
    inlines = (CommentsInline,)


class TagAdmin(DraggableMPTTAdmin):
    list_display = ('tree_actions', 'indented_title', 'id',)


admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Comment)
