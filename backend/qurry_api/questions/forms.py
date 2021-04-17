from django import forms
from django.core.exceptions import ValidationError
from media.models import Document, Image
from qurry_api.forms import BOOL_CHOICES, BaseActionForm, BaseModelForm

from .models import Answer, Comment, Question


class VotingFormMixin(forms.Form):
    VOTES_CHOICES = (
        ('1', '1'),
        ('0', '0'),
        ('-1', '-1'),
    )

    vote = forms.ChoiceField(choices=VOTES_CHOICES, required=False)

    def _validate_vote(self):
        vote = self.cleaned_data.get('vote')

        if vote:
            if self.user == self.instance.user:
                self.add_error('vote', ValidationError(
                    'Voting own posts is not allowed', code='own_post'))

    def _save_vote(self):
        vote = self.cleaned_data.get('vote')

        self.instance.remove_voter(self.user)
        if vote == '1':
            self.instance.got_voted(self.user, up=True)
        elif vote == '-1':
            self.instance.got_voted(self.user, up=False)


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
            if 'images' in self.fields:
                instance.add_images(self.cleaned_data.get('images'))
            if 'documents' in self.fields:
                instance.add_documents(self.cleaned_data.get('documents'))

        return instance


class CommentForm(BaseModelForm):

    class Meta:
        model = Comment
        fields = ('body', 'user', 'object_id', 'content_type')
        uneditable = ('user', 'object_id', 'content_type')


class QuestionActionForm(VotingFormMixin, BaseActionForm):

    subscribe = forms.ChoiceField(choices=BOOL_CHOICES, required=False)

    def _validate_subscribe(self):
        subscribe = self.cleaned_data.get('subscribe')
        did_subscribe = self.instance.is_subscriber(self.user)

        if subscribe == 'true' and did_subscribe:
            self.add_error('subscribe', ValidationError(
                'You already subscribed this item', code='subscribed_already'))

        if subscribe == 'false' and not did_subscribe:
            self.add_error('subscribe', ValidationError(
                'There is no subscribtion to cancel', code='no_subscribtion'))

    def _save_subscribe(self):
        subscribe = self.cleaned_data.get('subscribe')

        if subscribe == 'true':
            self.instance.get_subscribed_by(self.user)
        elif subscribe == 'false':
            self.instance.subscribtions.get(user=self.user).delete()


class AnswerActionForm(VotingFormMixin, BaseActionForm):
    pass
