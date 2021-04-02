from django import forms
from django.core.exceptions import ValidationError
from media.models import Document, Image
from qurry_api.forms import BaseModelForm

from .models import Answer, Comment, Question

BOOL_CHOICES = (
    (True, 'true'),
    (False, 'false'),
)


class VotingFormMixin(forms.Form):
    VOTES_CHOICES = (
        ('1', '1'),
        ('0', '0'),
        ('-1', '-1'),
    )

    vote = forms.ChoiceField(choices=VOTES_CHOICES, required=False)

    def vote_obj(self, user, obj, vote):
        if user == obj.user:
            self.add_error('vote', ValidationError(
                'Voting own posts is not allowed', code='own_post'))
        else:
            obj.remove_voter(user)
            if vote == '1':
                obj.got_voted(user, up=True)
            elif vote == '-1':
                obj.got_voted(user, up=False)


class QuestionForm(BaseModelForm):

    images = forms.ModelMultipleChoiceField(
        queryset=Image.objects.all(), required=False)
    documents = forms.ModelMultipleChoiceField(
        queryset=Document.objects.all(), required=False)

    class Meta:
        model = Question
        fields = ('title', 'body', 'user', 'tags')
        uneditable = ('user',)

    def save(self, commit=True):
        instance = super().save(commit=commit)
        if commit:
            instance.add_images(self.cleaned_data.get('images'))
            instance.add_documents(self.cleaned_data.get('documents'))

        return instance


class AnswerForm(BaseModelForm):

    images = forms.ModelMultipleChoiceField(
        queryset=Image.objects.all(), required=False)
    documents = forms.ModelMultipleChoiceField(
        queryset=Document.objects.all(), required=False)

    class Meta:
        model = Answer
        fields = ('body', 'question', 'user')
        uneditable = ('question', 'user')

    def save(self, commit=True):
        instance = super().save(commit=commit)

        if commit:
            # TODO: only add attachments when they are provided
            if self.cleaned_data.get('images'):
                instance.add_images(self.cleaned_data.get('images'))
            if self.cleaned_data.get('documents'):
                instance.add_documents(self.cleaned_data.get('documents'))

        return instance


class CommentForm(BaseModelForm):

    class Meta:
        model = Comment
        fields = ('body', 'user', 'object_id', 'content_type')
        uneditable = ('user', 'object_id', 'content_type')


class QuestionActionForm(VotingFormMixin, forms.Form):

    subscribe = forms.ChoiceField(choices=BOOL_CHOICES, required=False)

    def __init__(self, data, question, user, *args, **kwargs):
        super().__init__(data, *args, **kwargs)
        self.question = question
        self.user = user

    def clean(self):
        vote = self.cleaned_data.get('vote')
        if vote:
            self.vote_obj(self.user, self.question, vote)

        subscribe = self.cleaned_data.get('subscribe')
        if subscribe:
            self.subscribe_question(subscribe)

    def subscribe_question(self, subscribe):
        if subscribe == 'true':
            self.question.get_subscribed_by(self.user)

        else:
            try:
                self.question.subscribtion_set.get(user=self.user).delete()
            except:
                self.add_error('subscribe', ValidationError(
                    'There is no subscribtion to cancel', code='no_subscribtion'))


class AnswerActionForm(VotingFormMixin, forms.Form):
    def __init__(self, data, answer, user, *args, **kwargs):
        super().__init__(data, *args, **kwargs)
        self.answer = answer
        self.user = user

    def clean(self):
        vote = self.cleaned_data.get('vote')
        if vote:
            self.vote_obj(self.user, self.answer, vote)
