from django import forms
from django.contrib.auth.models import User
from uiforms.models import *

class UserRegisterForm(forms.Form):
    first_name = forms.CharField(max_length=128)
    last_name = forms.CharField(max_length=128)
    username = forms.CharField(max_length=32)
    email = forms.EmailField()
    password1 = forms.CharField(max_length=128, widget=forms.PasswordInput(render_value=False))
    password2 = forms.CharField(max_length=128, widget=forms.PasswordInput(render_value=False))

    def clean_username(self):
        try:
            User.objects.get(username=self.cleaned_data['username'])
        except User.DoesNotExist:
            return self.cleaned_data['username']
        raise forms.ValidationError("This username is unavailable.")

    def clean(self):
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError("Please type the same password twice.")
        return self.cleaned_data

    def save(self):
        new_user = User.objects.create_user(username=self.cleaned_data['username'],
                                            email=self.cleaned_data['email'],
                                            password=self.cleaned_data['password1'])
        new_user.first_name = self.cleaned_data['first_name']
        new_user.last_name = self.cleaned_data['last_name']
        new_user.save()
        return new_user

class UIFormFieldForm(forms.ModelForm):
    class Meta:
        model = UIFormField
        exclude = ['ui_form', 'created_at']

    def __init__(self, *args, **kwargs):
        self.parent_uiform = kwargs.pop('parent_uiform')
        super(UIFormFieldForm, self).__init__(*args, **kwargs)

    def save(self):
        uiform_field = super(UIFormFieldForm, self).save(commit=False)
        uiform_field.ui_form = self.parent_uiform
        uiform_field.save()

class UIFormForm(forms.ModelForm):
    class Meta:
        model = UIForm
        exclude = ['owner', 'created_at']

    def __init__(self, *args, **kwargs):
        self.owner = kwargs.pop('owner')
        super(UIFormForm, self).__init__(*args, **kwargs)

    def save(self):
        uiform = super(UIFormForm, self).save(commit=False)
        uiform.owner = self.owner
        uiform.save()
