from django import forms
from .models import Organisation, Organisateur
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

class OrganisateurForm1(forms.ModelForm):
  
  class Meta:
    model = Organisateur
    fields = ('prenom', 'nom', 'email')
    
  prenom = forms.CharField(widget=forms.TextInput(attrs={
      'class': 'form-control w-full rounded-lg h-[50px] border-0', 
      'id': 'prenom', 
      'placeholder': 'Prénom',
    }))
    
  nom = forms.CharField(widget=forms.TextInput(attrs={
      'class': 'form-control w-full rounded-lg h-[50px]', 
      'id': 'prenom', 
      'placeholder': 'Nom',
    }))
    
  email = forms.EmailField(widget=forms.EmailInput(attrs={
      'class': 'form-control w-full rounded-lg h-[50px]', 
      'id': 'email', 
      'placeholder': 'Adresse e-mail'
    }))

  def clean_email(self):
    email = self.cleaned_data['email']
    if User.objects.filter(username=email).exists():
      raise forms.ValidationError('Cette adresse e-mail est déjà utilisée')
    return email

class OrganisateurForm2(forms.ModelForm):
  
  password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control w-full h-[50px]', 'id': 'password1', 'placeholder': 'Mot de passe'}))
  password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control w-full h-[50px]', 'id': 'password2', 'placeholder': 'Confirmer le mot de passe'}))
  
  class Meta:
    model = Organisateur
    fields = ['password1', 'password2']

class OrganisationForm(forms.ModelForm):
  class Meta:
    model = Organisation
    fields = ['nom', 'description']
    widgets = {
      'nom': forms.TextInput(attrs={'class': 'form-control w-full h-[50px]', 'id': 'nom', 'placeholder': 'Nom de votre organisation'}),
      'description': forms.Textarea(attrs={'class': 'form-control w-full', 'id': 'description', 'placeholder': 'Donner une description claire de votre organisation'}),
    }

class OrganisateurLoginForm(forms.Form):
  email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'id': 'email', 'placeholder': 'Adresse e-mail'}))
  password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'id': 'password', 'placeholder': 'Mot de passe'}))