from django import forms
from .models import Student
from django.contrib.auth.models import User


import unicodedata
from django.contrib.auth import (
    authenticate, get_user_model, password_validation,
)
from django.contrib.auth.hashers import (
    UNUSABLE_PASSWORD_PREFIX, identify_hasher,
)
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMultiAlternatives
from django.template import loader
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.text import capfirst
from django.utils.translation import gettext, gettext_lazy as _
# from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
    class Meta:
        model =  User
        fields = ['username', 'password']

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'id':'id'})
        self.fields['password'].widget.attrs.update({'id':'pw'})

ONE = 1
TWO = 2
THREE = 3
FOUR = 4
FIVE = 5
SIX = 6
SEVEN = 7
EIGHT = 8

SELECTED_TALBE_CHOICES = (
    (ONE, '1'),
    (TWO, '2'),
    (THREE, '3'),
    (FOUR, '4'),
    (FIVE, '5'),
    (SIX, '6'),
    (SEVEN, '7'),
    (EIGHT, '8'),
)

class TableForm(forms.Form):
    selected_table = forms.ChoiceField(choices = SELECTED_TALBE_CHOICES,
    widget=forms.RadioSelect())


TIME_HOOBO = (
    ('1', '9 AM ~ 10 AM'),
    ('2', '10 AM ~ 11 AM'),
    ('3', '11 AM ~ 12 PM'),
    ('4', '11 PM ~ 12 PM'),
    ('5', '12 PM ~ 1 PM'),
    ('6', '1 PM ~ 2 PM'),
    ('7', '2 PM ~ 3 PM'),
    ('8', '3 PM ~ 4 PM'),
    ('9', '4 PM ~ 5 PM'),
)


class TimeForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(TimeForm, self).__init__(*args, **kwargs)
        time_selection = forms.MultipleChoiceField(
            required=False,
            widget=forms.CheckboxSelectMultiple,
            choices=TIME_HOOBO,
        )
    


class SetPasswordForm(forms.Form):
    error_messages = {
        'password_mismatch': _("두 비밀번호가 일치하지 않습니다. 다시 확인해 주세요"),
    }
    new_password1 = forms.CharField(
        label=_("새 비밀번호"),
        widget=forms.PasswordInput,
        strip=False,
    )
    new_password2 = forms.CharField(
        label=_("새 비밀번호 확인"),
        strip=False,
        widget=forms.PasswordInput,
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                )
        password_validation.validate_password(password2, self.user)
        return password2

    def save(self, commit=True):
        password = self.cleaned_data["new_password1"]
        self.user.set_password(password)
        if commit:
            self.user.save()
        return self.user


class PasswordChangeForm(SetPasswordForm):
    error_messages = {
        **SetPasswordForm.error_messages,
        'password_incorrect': _("이전 비밀번호가 올바르지 않습니다. 다시 시도해 주세요."),
    }
    old_password = forms.CharField(
        label=_("이전 비밀번호"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autofocus': True}),
    )

    field_order = ['old_password', 'new_password1', 'new_password2']

    def clean_old_password(self):
        old_password = self.cleaned_data["old_password"]
        if not self.user.check_password(old_password):
            raise forms.ValidationError(
                self.error_messages['password_incorrect'],
                code='password_incorrect',
            )
        return old_password


class custom_login_form(AuthenticationForm) :
        error_messages = {
        'invalid_login': _(
            "올바른 아이디와 패스워드를 입력해주세요"
        ),
        'inactive': _("This account is inactive."),
    }
