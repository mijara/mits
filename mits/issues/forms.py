from django import forms

from models import *


class IssueForm(forms.ModelForm):
    class Meta:
        model = Issue
        fields = ['name', 'description']


class IssueTagsForm(forms.ModelForm):
    class Meta:
        model = Issue
        fields = ['tags']
