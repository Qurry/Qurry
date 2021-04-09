from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import (AuthenticationForm, PasswordResetForm,
                                       UserChangeForm, UserCreationForm)
from django.core.exceptions import ValidationError

from .models import BlockedUser, ResetToken, User, clean_email_address


class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'username')

    def __init__(self, data, *args, **kwargs):
        if 'password1' not in data:
            data['password1'] = data.get('password')
            data['password2'] = data.get('password')
        super().__init__(data, *args, **kwargs)

    def check_blocked_user(self, email):
        if BlockedUser.objects.filter(email__iexact=email).exists():
            self.add_error('email', ValidationError(
                'This user is blocked. Please contact the support', code='blocked_user'))

    def clean(self):
        self.cleaned_data['email'] = clean_email_address(
            self.cleaned_data.get('email', ''))
        self.check_blocked_user(self.cleaned_data['email'])
        super().clean()


class AuthenticationForm(AuthenticationForm):
    def __init__(self, data=None, *args, **kwargs):
        if data and 'email' in data:
            data['username'] = data.get('email')
        return super().__init__(data=data, *args, **kwargs)

    def clean(self):
        self.cleaned_data['username'] = clean_email_address(
            self.cleaned_data.get('username', ''))
        super().clean()


class TokenValidationMixin:
    user_obj = User()
    token_obj = None

    error_messages = {
        'invalid_token': 'This link is invalid',
        'expired_token': 'This link is expired'
    }

    def invalid_token_error(self):
        raise ValidationError(
            self.error_messages['invalid_token'], code='invalid_token')

    def expired_token_error(self):
        raise ValidationError(
            self.error_messages['expired_token'], code='expired_token')

    def get_user(self):
        return self.user_obj

    def get_token(self):
        return self.token_obj


class TokenValidationForm(forms.Form, TokenValidationMixin):
    uid = forms.CharField(label='User ID')
    token = forms.CharField(label='Token')

    Model = None

    def __init__(self, data, token_class, *args, **kwargs):
        self.Model = token_class
        super().__init__(data, *args, **kwargs)

    def clean(self):
        uid = self.cleaned_data.get('uid')
        token = self.cleaned_data.get('token')

        try:
            self.user_obj = User.objects.get(id=uid)
            self.token_obj = self.Model.objects.get(user=uid, value=token)

        except (self.Model.DoesNotExist, User.DoesNotExist):
            raise self.invalid_token_error()
        else:
            if not self.token_obj.is_valid():
                raise self.expired_token_error()

        return self.cleaned_data


class PasswordForgotForm(forms.Form):
    email = forms.EmailField(label='E-Mail address')

    def clean(self):
        email = self.cleaned_data.get('email')
        try:
            self.user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise ValidationError(
                'This email address is invalid.', 'invalid_email_address')

        return self.cleaned_data


class PasswordResetForm(forms.Form, TokenValidationMixin):
    validation = forms.CharField(label='Validaiton Token')
    password = forms.CharField(label='New Password', strip=False)

    def clean(self):
        self.validate_token()
        self.validate_password()
        return self.cleaned_data

    def validate_password(self):
        password = self.cleaned_data.get('password')
        if password:
            try:
                password_validation.validate_password(password, self.user_obj)
            except ValidationError as error:
                self.add_error('password', error)

    def validate_token(self):
        validation = self.cleaned_data.get('validation')

        try:
            self.token_obj = ResetToken.objects.get(validation=validation)
            self.user_obj = self.token_obj.user

        except ResetToken.DoesNotExist:
            raise self.invalid_token_error()
        else:
            if self.token_obj.is_expired():
                raise self.expired_token_error()


class PasswordChangeForm(forms.Form):
    oldPassword = forms.CharField(
        label='Old Password', strip=False)
    newPassword = forms.CharField(
        label='new Password', strip=False)

    def __init__(self, data, instance=None, *args, **kwargs):
        self.instance = instance
        super().__init__(data, *args, **kwargs)

    def clean(self):
        super().clean()

        new_password = self.cleaned_data.get('newPassword')
        old_password = self.cleaned_data.get('oldPassword')

        if not self.instance.check_password(old_password):
            self.add_error('oldPassword', ValidationError(
                'Old Password is wrong', code='wrong_old_password'))

        password_validation.validate_password(
            new_password, self.instance)

    def save(self, commit=True):
        password = self.cleaned_data.get('newPassword')
        self.instance.set_password(password)

        if commit:
            self.instance.save()


class ProfileEditForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('username',)
