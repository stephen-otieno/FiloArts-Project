import password
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model, authenticate
from .models import Blog, Comment


User = get_user_model()

#login form
class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))



#registration form
class RegisterForm(forms.ModelForm):
    username = forms.CharField(
        max_length=150,
        help_text="",  # Remove help text
        widget=forms.TextInput(attrs={'class': 'form-control'})  # Optional

    )
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control'}),label='Email')
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password']


    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password')
        password2 = cleaned_data.get('confirm_password')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return cleaned_data



    def save(self, commit=True):
      user = super().save(commit=False)
      user.set_password(self.cleaned_data['password'])
      if commit:
            user.save()
            return user

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['image', 'description']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'text']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control col-md-4', 'placeholder': 'Enter your name'}),
            'text': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Write your comment...', 'rows': 4}),
        }




