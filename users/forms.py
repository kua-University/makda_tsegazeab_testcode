# from django import forms
# from django.contrib.auth.forms import UserCreationForm
# from .models import User
#
# class CustomUserCreationForm(UserCreationForm):
#     class Meta(UserCreationForm.Meta):
#         model = User  # Link to the custom User model
#         fields = ['username', 'email', 'is_student', 'is_admin']  # Add fields as per your needs
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator
from .models import User

class CustomUserCreationForm(UserCreationForm):
    # Custom validator for username
    username = forms.CharField(
        validators=[RegexValidator(regex='^[a-zA-Z0-9]*$', message='Username must be alphanumeric.')],
        max_length=150
    )
    age = forms.IntegerField(required=True)  # Add age field

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'email', 'age', 'is_student', 'is_admin', 'password1', 'password2']