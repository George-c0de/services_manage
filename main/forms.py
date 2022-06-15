from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm, Textarea, TextInput

from main.models import Organization


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class OrganizationForm(ModelForm):
    class Meta:
        model = Organization
        fields = ['name']
        labels = {
            'name': 'Название организации',
        }
        error_messages = {
            'name': {
                'max_length': "Название организации слишком длинное",
            },
        }
        widgets = {
            'name': TextInput(attrs={})
        }
