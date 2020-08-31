from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Novel
from .models import Team


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    email = forms.EmailField(max_length=254, required=True, help_text='To pole jest wymagane')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

class CreateTeamForm(forms.Form):
    required_css_class = 'required'
    team_name = forms.CharField(max_length=100, label='nazwa zespołu:', widget=forms.TextInput(attrs={'style': 'color: #27544F'}))

class MemberSearchForm(forms.Form):
    team_users = forms.CharField(label='nazwa użytkownika', max_length=200)



class CreateNovelForm(forms.Form):
    title = forms.CharField(max_length=200, label='Tytuł')
    content = forms.CharField(max_length=300, label='Wstęp')

class UpdateNovelForm(forms.Form):
    added_content = forms.CharField(max_length=300, label='Dopisz fragment', widget=forms.TextInput(attrs={'class': 'new_fragment','style': 'color: #27544F'}))




class SkipTurnForm(forms.Form):
    def __init__(self, all_members, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['current_user'] = forms.ChoiceField(label='Wybierz użytkownika, któremu chcesz przekazać kolejkę', choices=[])
        self.fields['current_user'].choices = ((user.pk, user.username) for user in all_members)


    # current_user = forms.ChoiceField(label='Wybierz użytkownika, któremu chcesz przekazać kolejkę', choices=[])

class EditNovelForm(forms.Form):
    content = forms.CharField(label='Wprowadź zmiany', initial=[], widget=forms.Textarea(attrs={'style': 'color: #27544F'}))


class PublishNovelForm(forms.Form):
    content = forms.CharField(label='Wprowadź ostatnie poprawki przed publikacją', initial=[], widget=forms.Textarea(attrs={'style': 'color: #27544F', 'class': 'materialize-textarea'}))


class CommentPublishedNovelForm(forms.Form):
    comment = forms.CharField(max_length=200, label='Dodaj komentarz')