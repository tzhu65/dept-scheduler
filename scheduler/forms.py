"""Django forms for passing in the spreadsheets.

The name of all the static fields are directly tied to the frontend client (typescript/react) and changes here would
require changes in the frontend. Otherwise, all the forms would fail on validation.
"""

from django import forms


class VerifySchedule(forms.Form):
    courses = forms.FileField(max_length=128, allow_empty_file=False)
    people = forms.FileField(max_length=128, allow_empty_file=False)
    faculty = forms.FileField(max_length=128, allow_empty_file=False)


class GenerateSchedule(forms.Form):
    courses = forms.FileField(max_length=128, allow_empty_file=False)
    people = forms.FileField(max_length=128, allow_empty_file=False)
    faculty = forms.FileField(max_length=128, allow_empty_file=False)
