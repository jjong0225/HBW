from django import forms
from .models import Student
from django.contrib.auth.models import User
# from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
    class Meta:
        model =  User
        fields = ['username', 'password']

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

