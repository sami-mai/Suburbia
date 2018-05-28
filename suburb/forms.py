from django.forms import Form, DecimalField, CharField
from django import forms
from .models import Resident, User


class EditSuburbForm(Form):
    suburb_name = CharField(max_length=80)
    latitude = DecimalField()
    longitude = DecimalField()


class EditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')


class EditProfile(forms.ModelForm):
    class Meta:
        model = Resident
        fields = ['avatar']
        exclude = ['user']
