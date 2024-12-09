from django import forms
from .models import Post
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

User = get_user_model()



class LoginForm(forms.Form):
    username = forms.CharField(label='Логин', max_length=255)
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)

class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'text', 'category', 'location', 'image')

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super().save(commit=False)
        print(self.user)
        if self.user:
            instance.author = self.user
        instance.pub_date = timezone.now()
        if commit:
            instance.save()
        return instance
    
class PostEditForm(PostForm):
    class Meta:
        model = Post
        fields = ('title', 'text', 'image', 'category', 'location')
    