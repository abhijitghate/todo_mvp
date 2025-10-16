from django import forms
from .models import Task


class TaskForm(forms.ModelForm):
    title = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "input input-bordered w-full",
                "placeholder": "Wite your task here...",
            }
        ),
    )

    completed = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={"class": "checkbox checkbox-primary"}),
    )

    class Meta:
        model = Task
        fields = ["title", "completed"]
