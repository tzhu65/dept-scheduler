from django import forms


class VerifySchedule(forms.Form):
    courses = forms.FileField(max_length=30, allow_empty_file=False)
    people = forms.FileField(max_length=30, allow_empty_file=False)
    faculty = forms.FileField(max_length=30, allow_empty_file=False)
