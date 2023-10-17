from django import forms
from .models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label="password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="confirm password", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ("email", "phone_number", "full_name")

    """In Django, forms have a built-in mechanism for cleaning and validating data before it is saved.
    Below method is automatically called when the form is submitted and is responsible for cleaning and
    validating the password2 field.
    """

    def clean_password2(self):
        cd = self.cleaned_data
        if cd["password1"] and cd["password2"] and cd["password1"] != cd["password2"]:
            raise ValidationError("passwords are not same.")
        return cd["password2"]

    def save(self, commit=True):
        user = super().save(commit=True)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(
        help_text='you can change password using <a href="../password/">this form</a>'
    )

    class Meta:
        model = User
        fields = ("email", "phone_number", "full_name", "password", "last_login")


class UserRegistrationForm(forms.Form):
    email = forms.EmailField()
    full_name = forms.CharField(label="full name")
    phone = forms.CharField(max_length=11)
    password = forms.CharField(widget=forms.PasswordInput)

    def clean_email(self):
        email = self.cleaned_data["email"]
        user = User.objects.filter(email=email).exists()
        if user:
            raise ValidationError("This email have been used by another user")
        return email

    def clean_phone(self):
        phone = self.cleaned_data["phone"]
        user = User.objects.filter(phone_number=phone).exists()
        if user:
            raise ValidationError("This phone number have been used by another user")
        return phone


class VerifyCodeForm(forms.Form):
    code = forms.IntegerField()

class VerifyLoginCodeForm(forms.Form):
    code = forms.IntegerField()

class UserLoginForm(forms.Form):
    phone_number = forms.CharField(max_length=11)
    password = forms.CharField(widget=forms.PasswordInput)

