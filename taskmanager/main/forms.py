
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Project, Task, Comment, Message

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'position', 'contact', 'avatar']

class ProjectForm(forms.ModelForm):
    members = forms.ModelMultipleChoiceField(queryset=User.objects.all(), widget=forms.CheckboxSelectMultiple)
    class Meta:
        model = Project
        fields = ['name', 'description', 'members']

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'project', 'due_date', 'priority', 'status', 'assignee']
        widgets = {
            'due_date': forms.TextInput(attrs={'id': 'id_due_date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['priority'].widget = forms.HiddenInput()
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']

class SearchForm(forms.Form):
    query = forms.CharField(required=False, label='Search', widget=forms.TextInput(attrs={'placeholder': 'Search...'}))

from django import forms

class TaskFilterForm(forms.Form):
    status = forms.ChoiceField(choices=[('', 'All'), ('new', 'New'), ('in_progress', 'In Progress'), ('completed', 'Completed')], required=False)
    priority = forms.ChoiceField(choices=[('', 'All'), ('low', 'Low'), ('medium', 'Medium'), ('high', 'High')], required=False)
    due_date = forms.DateField(required=False, widget=forms.TextInput(attrs={'type': 'date'}))
