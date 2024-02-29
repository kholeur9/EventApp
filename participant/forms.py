from django import forms
from .models import Participant
from django.contrib.auth.models import User


class ParticipantRegister(forms.ModelForm):
  class Meta:
    model = Participant
    fields = ['email']
    widgets = {
      'email': forms.EmailInput(attrs={'class': 'form-control', 'id': 'email'})
    }

class ParticipantRegister2(forms.ModelForm):
  password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control w-full h-[50px]', 'id': 'password1', 'placeholder': 'Mot de passe'}))
  password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control w-full h-[50px]', 'id': 'password2', 'placeholder': 'Confirmer le mot de passe'}))

  class Meta:
    model = Participant
    fields = ['password1', 'password2']

class ParticipantLoginForm(forms.Form):
  email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'id': 'email'}))
  password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'id': 'password'}))

class UpdateParticipant(forms.ModelForm):
  
  email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'id': 'email', 'read_only': 'read_only'}))
  first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'first_name'}))
  last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'id' : 'last_name'}))
  
  class Meta:
    model = Participant
    fields = ['phone', 'address', 'country', 'city', 'date_birth']
    widgets = {
      'phone': forms.TextInput(attrs={'class': 'form-control', 'id': 'phone'}),
      'address': forms.TextInput(attrs={'class': 'form-control', 'id': 'address'}),
      'country': forms.TextInput(attrs={'class': 'form-control', 'id': 'country'}),
      'city': forms.TextInput(attrs={'class': 'form-control', 'id': 'city'}),
      'date_birth': forms.TextInput(attrs={'class': 'form-control', 'id': 'date_birth'}),
    }


class UpdatePhoto(forms.ModelForm):
  class Meta:
    model = Participant
    fields = ['photo']
    widgits = {
      'photo': forms.FileInput(attrs={'class': 'form-control', 'id': 'photo', 'accept': 'image/*'})
    }