from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from .models import Participant
from evenement.models import Event

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as django_login
from django.contrib.auth import logout as auth_logout

from .forms import ParticipantLoginForm, ParticipantRegister, ParticipantRegister2, UpdateParticipant, UpdatePhoto

from social_django.models import UserSocialAuth
import requests

def register(request):
  if request.method == "POST":
    form = ParticipantRegister(request.POST)
    if form.is_valid():
      email = form.cleaned_data['email']
      if User.objects.filter(email=email).exists():
        return render(request, 'part-register.html', {'form': form, 'error': 'Adresse email déjà utilisée'})
      else:
        request.session['email_register'] = email
        return redirect('participant:secure-compte')
  else:
    initialDatas = {'email': request.session.get('email_register', '')}
    form = ParticipantRegister(initial=initialDatas)
  return render(request, 'part-register.html', {'form': form})

def secure_compte(request):
  if 'email_register' not in request.session:
    return redirect('participant:register')

  email = request.session['email_register']

  if request.method == "POST":
    form = ParticipantRegister2(request.POST)
    if form.is_valid():
      password1 = form.cleaned_data['password1']
      password2 = form.cleaned_data['password2']

      if password1 != password2:
        return render(request, 'part-register2.html', {'form': form, 'error': 'Les mots de passe ne correspondent pas'})
        
      elif len(password1) < 8:
        return render(request, 'part-register2.html', {'form': form, 'error': 'Le mot de passe doit contenir au moins 8 caractères'})

      else:
        try:
          user = User.objects.create_user(username=email, email=email, password=password1)
          user_social = UserSocialAuth.objects.filter(user=user, provider='google-oauth2').exists()
          if not user_social:
            participant_create = Participant.objects.create(user=user, email=email)
            return redirect('participant:home_view')
          else:
            return render(request, 'part-register2.html', {'form': form, 'error': 'Vous avez déjà un compte'})
        except Exception as e:
          print(f"An error occured: {e}")
          return render(request, 'part-register2.html', {'form': form, 'error': 'Une erreur est survenue, veuillez réessayer'})

  else:
    form = ParticipantRegister2()
    
  return render(request, 'part-register2.html', {'form': form})

def login_view(request):
  if request.method == "POST":
    form = ParticipantLoginForm(request.POST)
    if form.is_valid():
      email = form.cleaned_data['email']
      password = form.cleaned_data['password']
      user = authenticate(request, username=email, password=password)
      if user is not None:
        django_login(request, user)
        try:
          return redirect('participant:home_view')
        except Participant.DoesNotExist:
          return render(request, 'login.html', {'form': form, 'error': 'Vous n\'êtes pas inscrit'})
      else:
        return render(request, 'login.html', {'form': form, 'error': 'Identifiants invalides' })
  else:
    form = ParticipantLoginForm()
  return render(request, 'login.html', {'form': form})

def logout_view(request):
  auth_logout(request)
  return redirect('participant:login_view')

@login_required
def home_view(request):
  user = request.user
  participant = Participant.objects.get(user=user)
  events_confirmed = Event.objects.filter(status='confirmé')
  return render(request, 'profile.html', {'user': user, 'participant': participant, 'events_confirmed': events_confirmed})

@login_required
def profile_user(request):
  user = request.user
  take_current_page = request.path
  current_page = take_current_page == '/participant/profile-user/'
  participant = Participant.objects.get(user=user)
  
  pro_user = None
  if current_page:
    pro_user = participant.user.first_name

  if request.method == "POST" and request.is_ajax():
    form = UpdatePhoto(request.POST, request.FILES, instance=participant)
    if form.is_valid():
      photo = form.cleaned_data['photo']
      partcipant.user = photo
      participant.save()
      return JsonResponse({'photo': photo.photo.url})

  else:
    form = UpdatePhoto(instance=participant)
    
  return render(request, 'profile-user.html', {'form': form, 'user': user, 'pro_user': pro_user, 'participant': participant})

@login_required
def informations(request, participant_id):
  
  participant = get_object_or_404(Participant, id=participant_id)
  
  user = request.user
  current_page = request.path == '/participant/informations/' + str(participant_id) + '/'
  
  pro_user = None
  if current_page:
    pro_user = 'Informations'

  if request.method == "POST":
    form = UpdateParticipant(request.POST)
    if form.is_valid():
      participant.user.email = form.cleaned_data['email']
      participant.user.first_name = form.cleaned_data['first_name']
      participant.user.last_name = form.cleaned_data['last_name']
      participant.phone = form.cleaned_data['phone']
      participant.address = form.cleaned_data['address']
      participant.country = form.cleaned_data['country']
      participant.city = form.cleaned_data['city']
      participant.date_birth = form.cleaned_data['date_birth']
      participant.user.save()
      participant.save()
      return render(request, 'informations.html', {'form': form, 'user': user, 'pro_user': pro_user, 'participant': participant, 'success': 'Vos informations ont bien été modifiées'})

  else:
    initial_data = {
      'email': participant.user.email,
      'first_name': participant.user.first_name,
      'last_name': participant.user.last_name,
      'phone': participant.phone,
      'address': participant.address,
      'country': participant.country,
      'city': participant.city,
      'date_birth': participant.date_birth
    }
    
    form = UpdateParticipant(initial=initial_data)
  
  context = {
    'user': user,
    'pro_user': pro_user,
    'form': form,
  }
  return render(request, 'informations.html', context)