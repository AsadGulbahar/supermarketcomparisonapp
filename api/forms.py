from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from django.forms.widgets import TextInput, EmailInput, PasswordInput

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(required=True, help_text="Required.", widget=TextInput(attrs={'placeholder': 'Username'}))
    email = forms.EmailField(label="Email", required=True, help_text="Required. Add a valid email address.", widget=EmailInput(attrs={'placeholder': 'Email Address'}))
    password1 = forms.CharField(
        label="Password",
        widget=PasswordInput(attrs={'autocomplete': 'new-password', 'placeholder': 'Password'}),
        help_text="Your password can't be too similar to your other personal information."
    )
    password2 = forms.CharField(
        label="Password confirmation",
        widget=PasswordInput(attrs={'autocomplete': 'new-password', 'placeholder': 'Confirm Password'}),
        help_text="Enter the same password as above, for verification."
    )
    first_name = forms.CharField(required=True, widget=TextInput(attrs={'placeholder': 'First Name'}))
    last_name = forms.CharField(required=True, widget=TextInput(attrs={'placeholder': 'Last Name'}))
    address = forms.CharField(required=False, widget=forms.Textarea(attrs={'placeholder': 'Address', 'rows': 2}), help_text="Optional.")

    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name", "profile_image", "address")

 

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'autofocus': True}))
    password = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'}),
    )
