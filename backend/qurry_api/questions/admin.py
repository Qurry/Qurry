from django.contrib import admin

from .models import Question, Answer, Tag

class AnwersInline(admin.TabularInline):
    model = Answer

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'user', )
    readonly_fields = ('id', )
    filter_horizontal = ('tags', 'vote_up_users', 'vote_down_users')
    inlines = (AnwersInline, )

admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer)
admin.site.register(Tag)
