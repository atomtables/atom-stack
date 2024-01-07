from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


# Create your forms here.

class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.Field(label="First Name")
    last_name = forms.Field()

    class Meta:
        model = User
        fields = ("first_name", "last_name", "username", "email", "password1", "password2")

    def clean_email(self):
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')

        if email and User.objects.filter(email=email).exclude(username=username).count():
            raise forms.ValidationError(
                'This email address is already in use. Please supply a different email address.')
        return email

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user


class EditNameForm(forms.ModelForm):
    first_name = forms.Field(label="First Name")
    last_name = forms.Field(label="Last Name")

    class Meta:
        model = User
        fields = ("first_name", "last_name")

    def save(self, commit=True):
        user = super(EditNameForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user


class EditEmailForm(forms.ModelForm):
    email = forms.Field(label="Email")

    class Meta:
        model = User
        fields = ("email",)

    def save(self, commit=True):
        user = super(EditEmailForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class EditBioForm(forms.ModelForm):
    bio = forms.Field(label="Bio", widget=forms.Textarea(attrs={'type': 'large-text'}), required=False)

    class Meta:
        model = User
        fields = ("bio",)

    def save(self, commit=True):
        user = super(EditBioForm, self).save(commit=False)
        user.profile.bio = self.cleaned_data['bio']
        if commit:
            user.save()
        return user


class EditPFPForm(forms.ModelForm):
    profile_picture = forms.ImageField(label="Profile Picture")

    class Meta:
        model = User
        fields = ("profile_picture",)

    def save(self, commit=True):
        user = super(EditPFPForm, self).save(commit=False)
        user.profile.profile_picture = self.cleaned_data['profile_picture']
        if commit:
            user.save()
        return user
