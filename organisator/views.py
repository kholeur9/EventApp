from django.shortcuts import render, redirect, get_object_or_404
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import OrganisateurForm1, OrganisateurForm2, OrganisationForm, OrganisateurLoginForm
from django.contrib.auth.models import User
from .models import Organisation, Organisateur

# Create your views here.

# Etape 1 : Création de l'organisateur
def etape_1(request):
  
  if request.method == 'POST':
    form = OrganisateurForm1(request.POST)
    
    if form.is_valid():
      email = request.POST.get('email')
      if User.objects.filter(email=email).exists():
        return render(request, 'organ-login.html', {'form': form, 'error': 'Email déjà utilisé'})
        
      request.session['etape1'] = form.cleaned_data
      request.session['prenom'] = form.cleaned_data['prenom']
      request.session['nom'] = form.cleaned_data['nom']
      request.session['email'] = form.cleaned_data['email']
      
      try:
        return redirect('organisator:secure-compte')
      except IntegrityError:
        return render(request, 'organ-login.html', {'form': form, 'error': 'Cette adresse email existe déjà.'})

  else:
    initialData = {
      'prenom': request.session.get('prenom', ''),
      'nom': request.session.get('nom', ''),
      'email': request.session.get('email', ''),
    }
    form = OrganisateurForm1(initial=initialData)
    
  return render(request, 'organ-login.html', {'form' : form})


# Etape 2 : Enregistrement de l'organisateur
def secure_compte(request):
  if 'etape1' not in request.session:
    return redirect('organisator:etape-1')
  etape1 = request.session['etape1']
  
  if request.method == 'POST':
    form = OrganisateurForm2(request.POST)
    if form.is_valid(): 
      form_data = {**etape1, **form.cleaned_data}
      
      if form_data['password1'] != form_data['password2']:
        return render(request, 'organ-login2.html', {'form': form, 'error': 'Les mots de passe ne correspondent pas'})

      elif form_data['password1'] == '' or form_data['password2'] == '':
        return render(request, 'organ-login2.html', {'form': form, 'error': 'Les champs ne peuvent pas être vides'})

      elif len(form_data['password1']) < 8 or len(form_data['password2']) < 8:
        return render(request, 'organ-login2.html', {'form': form, 'error': 'Le mot de passe doit contenir au moins 8 caractères', 'back': 'etape-1'})
        
      request.session['etape2'] = form_data
      try:
        return redirect('organisator:register-organisation')
      except:
        return render(request, 'organ-login2.html', {'form': form, 'error': 'Erreur avec vos identifiants'})
  
  else:
    form = OrganisateurForm2()
  
  return render(request, 'organ-login2.html', {'form': form, 'etape1': etape1, 'back': 'etape-1'})


def register_organisation(request):
  if 'etape2' not in request.session:
    return redirect('organisator:secure-compte')
  etape2 = request.session['etape2']
  
  if request.method == 'POST':
    form = OrganisationForm(request.POST)
    if form.is_valid():
      get_nom = form.cleaned_data['nom']
      description = form.cleaned_data['description']
      check_nom = Organisation.objects.filter(nom=get_nom).exists()
      if check_nom:
        return render(request, 'register-organisation.html', {'form': form, 'error': 'Cette organisation existe déjà'})
      else:
        try:
          user = User.objects.create_user(
            username=etape2['email'], 
            first_name=etape2['prenom'], 
            last_name=etape2['nom'],
            email=etape2['email'],
            password=etape2['password1']
          )
          
          organisateur = Organisateur.objects.create(user=user, prenom=etape2['prenom'], nom=etape2['nom'], email=etape2['email'])
          createur = User.objects.get(username=etape2['email'])
          organisation = Organisation.objects.create(nom=get_nom, description=description, createur=createur)
          organisateur.organisations_crees.add(organisation)
          
          #get_id = Organisateur.objects.get(user=user)
          del request.session['etape1']
          del request.session['etape2']
          del request.session['prenom']
          del request.session['nom']
          del request.session['email']
          return redirect('organisator:dashboard', organisatorID=organisateur.id)
        except Exception as e:
          return render(request, 'register-organisation.html', {'form': form, 'back': 'secure-compte', 'error': e})

  else:
    form = OrganisationForm()
      
  return render(request, 'register-organisation.html', {'form': form, 'back': 'secure-compte'})


def connexion(request):
  if request.method == "POST":
    form = OrganisateurLoginForm(request.POST)
    if form.is_valid():
      email = form.cleaned_data['email']
      password = form.cleaned_data['password']
      user = authenticate(request, username=email, password=password)
      if user is not None:
        login(request, user)
        try:
          organisateur = Organisateur.objects.get(user=user)
          return redirect('organisator:dashboard', organisatorID=organisateur.id)
        except Organisateur.DoesNotExist:
          return render(request, 'connexion.html', {'form': form, 'error': 'Organisateur non trouvé dans Event.'})
      else:
        return render(request, 'connexion.html', {'form': form, 'error': 'Identifiants: email ou mot de passe incorrects.'})
  else:
    form = OrganisateurLoginForm()
    
  return render(request, 'connexion.html', { 'form': form })


def deconnexion(request):
  logout(request)
  return redirect('organisator:connexion')


@login_required(login_url='/organisateur/connexion')
def dashboard(request, organisatorID):
  organisator = get_object_or_404(Organisateur, id=organisatorID)
  context = {
    'organisator': organisator,
  }
  return render(request, 'dashboard.html', context=context)