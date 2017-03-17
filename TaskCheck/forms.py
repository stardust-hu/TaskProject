# -*- coding: utf-8 -*-
from django import forms
from .models import PersonTask


class AddPersonTask(forms.ModelForm):
    class Meta:
        model = PersonTask
        fields = ['date', 'person', 'task', 'is_solve']


if __name__ == '__main__':
    pass
