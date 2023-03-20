from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.images import get_image_dimensions
from django.forms import ModelForm, modelformset_factory, Textarea, Select, NumberInput, CharField, TextInput, \
    inlineformset_factory, formset_factory

from django import forms

from user_app.models import Role
from .models import *


class UserHouseForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['user']
        exclude = ['role']

    user = forms.ModelChoiceField(
        required=False,
        widget=forms.Select(
            attrs={'class': 'form-control', 'onchange': "selectUser(this)"}),
        queryset=UserProfile.objects.all(),
        empty_label = "Выберите...")

    role = forms.CharField(required=False, initial='Выберите...',
        widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'true'}))

    # def clean_role(self):
    #     print(self.cleaned_data)
    #     data = self.cleaned_data['role']
    #     try:
    #         return Role.objects.get(roles=data)
    #     except ObjectDoesNotExist:
    #         raise forms.ValidationError("Роль не найдена")
    #     return data



UserFormSet  = formset_factory(form=UserHouseForm, extra=0, can_delete=True)

class SectionForm(forms.ModelForm):
    class Meta:
        model = Section
        exclude = ('house',)


SectionFormSet = modelformset_factory(Section, form=SectionForm, extra=0, can_delete=True)


class FloorForm(forms.ModelForm):
    class Meta:
        model = Floor
        exclude = ('house',)


FloorFormSet = modelformset_factory(Floor, form=FloorForm, extra=0, can_delete=True)


class ApartmentForm(forms.ModelForm):
    class Meta:
        model = Apartment
        fields = '__all__'
        widgets = {
            'number': forms.TextInput(attrs={'class': 'form-control'}),
            'area': forms.TextInput(attrs={'class': 'form-control'}),
            'house': forms.Select(attrs={'class': 'form-control'}),
            'section': forms.Select(attrs={'class': 'form-control'}),
            'floor': forms.Select(attrs={'class': 'form-control'}),
            'owner': forms.Select(attrs={'class': 'form-control'}),
            'tariff': forms.Select(attrs={'class': 'form-control'}),

        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['house'].empty_label = 'Выберите дом'
        self.fields['tariff'].empty_label = 'Выберите...'
        self.fields['owner'].empty_label = 'Выберите...'
        self.fields['section'].empty_label = 'Выберите...'
        try:
            if self.instance.house.id:
                self.fields['section'].queryset = Section.objects.filter(house_id=self.instance.house.id)
                self.fields['floor'].queryset = Floor.objects.filter(house_id=self.instance.house.id)
        except:
            self.fields['section'].queryset = Section.objects.all()
            self.fields['floor'].queryset = Floor.objects.all()
        self.fields['floor'].empty_label = 'Выберите...'




class HouseForm(forms.ModelForm):

    class Meta:
        model = House
        fields = '__all__'
        exclude = ('users',)
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'image_1': forms.FileInput(attrs={'type': 'file'}),
            'image_2': forms.FileInput(attrs={'type': 'file'}),
            'image_3': forms.FileInput(attrs={'type': 'file'}),
            'image_4': forms.FileInput(attrs={'type': 'file'}),
            'image_5': forms.FileInput(attrs={'type': 'file'}),
        }

    def clean(self):
        images = ['image_1', 'image_2', 'image_3', 'image_4', 'image_5']
        for image in images:
            if self.cleaned_data[image]:
                width, height = get_image_dimensions(self.cleaned_data[image])
                if image == 'image_1':
                    if width != 522 or height != 350:
                        raise forms.ValidationError("Размеры изображения не валидны (522x350)")
                else:
                    if width != 248 or height != 160:
                        raise forms.ValidationError("Размеры изображения не валидны (248x160)")
        return self.cleaned_data

class RequestForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = '__all__'