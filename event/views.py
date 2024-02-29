from django.shortcuts import render

def index(request):
  return render(request, 'home.html')

def credit(request):
  return render(request, 'credit.html')