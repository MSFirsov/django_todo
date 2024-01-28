from django import forms
from .models import Task


class CreateTaskForm(forms.ModelForm):
    task_date = forms.DateInput()

    class Meta:
        model = Task
        fields = ['text', 'task_date', 'is_completed', 'user']
        widgets = {
            'text': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите текст задания'}),
        }
