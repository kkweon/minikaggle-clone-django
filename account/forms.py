from django import forms
from django.contrib.auth import get_user_model, password_validation

User = get_user_model()


class RegisterForm(forms.ModelForm):
    email = forms.EmailField(label="Email", required=True)
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Confirm password", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password",
            "password2",
        ]

    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if email and User.objects.filter(email=email).exclude(
                username=username).exists():
            raise forms.ValidationError(u'Email address already exists')
        return email

    def clean_password2(self):
        first_pw = self.cleaned_data.get("password")
        second_pw = self.cleaned_data.get("password2")

        if first_pw and second_pw and first_pw != second_pw:
            raise forms.ValidationError("Passwords do not match!")
        password_validation.validate_password(second_pw, self.instance)
        return second_pw

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password2"])
        if commit:
            user.save()
        return user
