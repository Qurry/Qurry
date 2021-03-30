from django import forms
from media.models import Document, Image
from qurry_api.forms import BaseModelForm

from .models import Answer, Comment, Question


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
