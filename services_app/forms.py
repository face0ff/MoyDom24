from django.contrib.auth.models import User
from django.forms import ModelForm, modelformset_factory, Textarea, FileInput, CheckboxInput, CharField, TextInput
from django import forms
from .models import *


class ServicesForm(forms.ModelForm):
    class Meta:
        model = Services
        fields = '__all__'


ServicesFormSet = modelformset_factory(model=Services, form=ServicesForm, extra=0, can_delete=True)


class UnitForm(forms.ModelForm):
    class Meta:
        model = Unit
        fields = '__all__'


UnitFormSet = modelformset_factory(model=Unit, form=UnitForm, extra=0, can_delete=True)


class TariffForm(forms.ModelForm):
    class Meta:
        model = Tariff
        fields = '__all__'

class PriceTariffServicesForm(forms.ModelForm):

    currency = forms.CharField(required=False, initial='грн',
                               widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'true'}))

    unit = forms.CharField(required=False, initial='Выберите...',
                               widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'true'}))

    def __init__(self, *args, **kwargs):
        super(PriceTariffServicesForm, self).__init__(*args, **kwargs)
        if kwargs.get('instance'):
            self.fields['unit'].initial = kwargs.get('instance').services.unit.name

    class Meta:
        model = PriceTariffServices
        exclude = ['tariff']
        widgets = {
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'services': forms.Select(attrs={'class': 'form-control',
                                            'onchange': "selectServices(this)"})
        }


PriceTariffServicesFormset = modelformset_factory(model=PriceTariffServices, form=PriceTariffServicesForm, extra=0, can_delete=True)


class RequisiteForm(forms.ModelForm):
    class Meta:
        model = Requisite
        fields = '__all__'


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = '__all__'
