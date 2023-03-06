from django.contrib.auth.models import User
from django.forms import ModelForm, modelformset_factory, Textarea, FileInput, CheckboxInput, CharField, TextInput
from django import forms
from .models import *


class ApartmentForm(forms.ModelForm):
    class Meta:
        model = Apartment
        fields = '__all__'

class HouseForm(forms.ModelForm):
    class Meta:
        model = House
        fields = '__all__'

