from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import (
    authenticate, get_user_model, password_validation,
)
from django.core.exceptions import ValidationError
from .models import User
from django import forms


class UserCreationForm(forms.ModelForm):

    password = forms.CharField(
        label='Password',
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        help_text=password_validation.password_validators_help_text_html(),
    )

    class Meta:
        model = User
        fields = ('email' ,'username')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self._meta.model.USERNAME_FIELD in self.fields:
            self.fields[self._meta.model.USERNAME_FIELD].widget.attrs['autofocus'] = True

    def clean_password(self):
        password = self.cleaned_data.get("password")
        return password

    def _post_clean(self):
        super()._post_clean()
        # Validate the password after self.instance is updated with form data
        # by super().
        password = self.cleaned_data.get('password')
        if password:
            try:
                password_validation.validate_password(password, self.instance)
            except ValidationError as error:
                self.add_error('password', error)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class UserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = ('email', 'username')