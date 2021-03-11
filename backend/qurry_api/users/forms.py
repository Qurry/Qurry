from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserChangeForm
from django.core.exceptions import ValidationError

from .models import User
from .validators import HPIEmailValidator


class UserCreationForm(forms.ModelForm):
    password = forms.CharField(
        label='Password',
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        help_text=password_validation.password_validators_help_text_html(),
    )

    class Meta:
        model = User
        fields = ('email', 'username')

    def validate_password(self, password, *args):
        password_validation.validate_password(password, *args)

    def clean_password(self):
        password = self.cleaned_data.get('password')
        return password

    def _post_clean(self):
        super()._post_clean()
        email = self.cleaned_data.get('email')
        if email:
            try:
                HPIEmailValidator()(email)
            except ValidationError as error:
                self.add_error('email', error)
        # Validate the password after self.instance is updated with form data
        # by super().
        password = self.cleaned_data.get('password')
        if password:
            try:
                self.validate_password(password, self.instance)
            except ValidationError as error:
                self.add_error('password', error)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class UserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('email', 'username')
