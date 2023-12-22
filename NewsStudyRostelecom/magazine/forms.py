from django import forms
from .models import Demo
from django.forms.widgets import TextInput, FileInput

class DemoForm(forms.ModelForm):
    class Meta:

        model = Demo
        fields = ('title', 'image')
        widgets={
            'title': TextInput(attrs={'class':'input','placeholder':'Заголовок'}),
            'image': FileInput(attrs={'class': 'input', 'placeholder': 'image'}),
        }