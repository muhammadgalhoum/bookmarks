import re, datetime
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from.models import Contact

User = get_user_model()


class EmailValidationMixin:
    def clean_email(self):
        email = self.cleaned_data.get('email')
        user_queryset = User.objects.filter(email=email)

        # Exclude the current instance only if it exists (editing case)
        if self.instance and self.instance.pk:
            user_queryset = user_queryset.exclude(pk=self.instance.pk)

        if user_queryset.exists():
            raise forms.ValidationError("This email is already taken.")

        return email


class UserRegistrationForm(forms.ModelForm, EmailValidationMixin):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Repeat Password', widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if password != password2:
            raise forms.ValidationError("Passwords don't match.")

        regex = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[_#@$])[A-Za-z\d_#@$!=]{8,}$'

        if not re.match(regex, password):
            raise forms.ValidationError(
                "Required. 8 characters or more. Letters, digits and _#@$ only.")

        return cleaned_data

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']


class ContactCreationForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['user_from', 'user_to']


class ContactChangeForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = "__all__"    
        
        
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email']


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = "__all__"


class UserEditForm(forms.ModelForm, EmailValidationMixin):
    date_of_birth = forms.DateField(
        widget=forms.SelectDateWidget(
            years=range(datetime.datetime.now().year - 100, datetime.datetime.now().year + 1),
            attrs={
                'class': 'form-control date-select',
                'style': 'width: auto; display: inline-block; margin-right: 5px;'
            }
        ),
        required=False
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'date_of_birth', 'photo']
        widgets = {
            'photo': forms.FileInput(attrs={'class': 'form-control-file'}),
        }
