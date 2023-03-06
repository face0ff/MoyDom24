import re

from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError
from django.forms import ModelForm, modelformset_factory

from user_app.models import Role, UserProfile


class RoleForm(ModelForm):
    class Meta:
        model = Role
        exclude = ('role',)


RoleFormSet = modelformset_factory(Role, form=RoleForm, extra=0)

class UserForm(UserCreationForm):

    class Meta:
        model = UserProfile
        fields = ['email', 'first_name', 'last_name', 'status', 'role', 'telephone', 'password1', 'password2']

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError(self.error_messages['password_mismatch'], code='password_mismatch')
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.is_active = True
        user.status = 'new'
        if commit:
            user.save()
        return user


class UserUpdateForm(UserChangeForm):
    password1 = forms.CharField(required=False, label='Пароль')
    password2 = forms.CharField(required=False, label='Повторить пароль')
    class Meta:
        model = UserProfile
        fields = ['email', 'first_name', 'last_name', 'telephone', 'password1', 'password2']
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if not password1 and not password2:
            pass
        else:
            if password1 and password2 and password1 != password2:
                raise ValidationError(self.error_messages['password_mismatch'], code='password_mismatch')
            return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        if not self.cleaned_data['password1']:
            if commit:
                user.save()
            return user
        else:
            user.set_password(self.cleaned_data['password1'])
            if commit:
                user.save()
            print('celery')
            return user