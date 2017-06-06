from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import (
    authenticate,
	get_user_model,
	login,
	logout,
)
from models import Post, Tag

User = get_user_model()

class RegistrationForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    first_name= forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name= forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    email= forms.CharField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password1= forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2= forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2'
        )
        ''' widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'})
        }'''



    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)


        if commit:
            user.save()

        return user

class UserLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))


    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError("This user does not exist")
            if not user.check_password(password):
                raise forms.ValidationError("Incorrect passowrd")
            if not user.is_active:
                raise forms.ValidationError("This user is not longer active.")
            return super(UserLoginForm, self).clean(*args, **kwargs)


class UserRegisterForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='Email address', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    email2 = forms.EmailField(label='Confirm Email', widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'email2',
            'password'
        ]

    def clean_email(self):
        email = self.cleaned_data.get('email')
        email2 = self.cleaned_data.get('email')
        print(email, email2)
        if email != email2:
            raise forms.ValidationError("Emails must match")
        email_qs = User.objects.filter(email=email)
        if email_qs.exists():
            raise forms.ValidationError("This email has already been registered")
        return email

class PostAddForm(forms.ModelForm):
    tytul = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}),required=False)
    haslo = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}),required=False)
    skrocona_tresc = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}),required=False)
    tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.all(),required=False)
    obrazek_postu = forms.FileField()
    class Meta:
        model = Post
        fields = [
            'tytul',
            'haslo',
            'skrocona_tresc',
            'tags',
            'obrazek_postu'
        ]


    # def __init__(self, *args, **kwargs):
    #     super(PostAddForm, self).__init__(*args, **kwargs)
    #     self.fields["tagi"].initial = (
    #         Tag.objects.all().values_list(
    #             'id', flat=True
    #         )
    #     )
    # def clean(self):
    #    cleaned_data = super(PostAddForm, self).clean()
    #    data = self.cleaned_data
    #    data['tags'] = self.tags
    #    return data
    # def clean_tytul(self):
    #     tytul = self.cleaned_data.get("tytul")
    #     haslo = self.cleaned_data.get("haslo")
    #     skrocona_tresc = self.cleaned_data.get("skrocona_tresc")
    #     tags = self.cleaned_data.get("tags")
    #     return tytul,haslo,skrocona_tresc,tags
    # def clean(self):
    #     cleaned_data = super(PostAddForm, self).clean()
    #     tags = self.cleaned_data.get("tagi")
    #     if not tags:
    #         raise forms.ValidationError('Tagi field is required.')
    #     return self.cleaned_data