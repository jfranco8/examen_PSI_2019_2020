from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class SignupForm(forms.ModelForm):
    """
    A form that creates a user, with no privileges, from the given username and
    password.
    """
    username = forms.CharField(label="Username", required=True)

    password = forms.CharField(label=("Password"), required=True,
                               widget=forms.PasswordInput)
    password2 = forms.CharField(label=("Repeat password"), required=True,
                                widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ("username", "password", "password2")

    def clean_password2(self):
        password1 = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                "Password and Repeat password are not the same|"
                "La clave y su repetición no coinciden"
            )
        return password2

    def clean_password(self):
        password1 = self.cleaned_data.get("password")
        if len(password1) < 6:
            raise ValidationError(
                "password too common or password is too short "
                "make sure it has at least 6 characters")
        return password1


class MoveForm(forms.ModelForm):
    origin = forms.IntegerField(min_value=0, max_value=63, required=False,
                                label="Origin: ")
    target = forms.IntegerField(min_value=0, max_value=63, required=False,
                                label="Target: ")

    class Meta:
        model = User
        fields = ("origin", "target")

    # def bad_move(self):
    #     raise ValidationError(
    #          "Move not allowed|Movimiento no permitido")
