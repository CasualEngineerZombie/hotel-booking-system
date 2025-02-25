from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        "id": "email",
        "autocomplete": "email",
        "required": True,
        "class": ("appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md "
                  "shadow-sm placeholder-gray-400 focus:outline-none focus:ring-blue-500 "
                  "focus:border-blue-500 sm:text-sm"),
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        "id": "password",
        "autocomplete": "current-password",
        "required": True,
        "class": ("appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md "
                  "shadow-sm placeholder-gray-400 focus:outline-none focus:ring-blue-500 "
                  "focus:border-blue-500 sm:text-sm"),
    }))

class RegistrationForm(UserCreationForm):
    full_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            "id": "name",
            "autocomplete": "name",
            "class": "appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm",
        })
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            "id": "email",
            "autocomplete": "email",
            "class": "appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm",
        })
    )
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={
            "id": "password",
            "autocomplete": "new-password",
            "class": "appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm",
        })
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={
            "id": "password2",
            "autocomplete": "new-password",
            "class": "appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm",
        })
    )

    class Meta:
        model = User
        # We use full_name and email instead of a separate username field.
        fields = ("full_name", "email", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        full_name = self.cleaned_data.get("full_name")
        email = self.cleaned_data.get("email")
        user.username = email  # Use email as the username
        user.first_name = full_name  # Store full name in first_name (or split as needed)
        user.email = email
        if commit:
            user.save()
        return user
