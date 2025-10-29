# forms.py
from django import forms
from django.contrib.auth.models import User

class StaffCreationForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput,
        help_text="Password must be exactly 8 characters long."
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) != 8:
            raise forms.ValidationError("Password should be exactly 8 digits.")
        return password

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])  # Encrypt password
        user.is_staff = True  # Mark as staff
        if commit:
            user.save()
        return user
