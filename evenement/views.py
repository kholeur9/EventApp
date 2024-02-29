from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from .models import Categorie, Event, Favoris
from ticket.models import Ticket

def favoris_add(request, pk):
  event = get_object_or_404(Event, pk=pk)
  favoris, created = Favoris.objects.get_or_create(user=request.user, event=event)
  if created:
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
  else:
    favoris.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def detail_event(request, pk):
  is_favoris = False
  event = get_object_or_404(Event, pk=pk)
  idem_category = Event.objects.filter(category=event.category, is_sold_out=False).exclude(pk=pk)
  is_favoris = Favoris.objects.filter(user=request.user, event=event)
  tickets = Ticket.objects.filter(event=event)
  context = {
    'event': event,
    'idem_category': idem_category,
    'is_favoris': is_favoris,
    'tickets': tickets,
  }
  return render(request, 'detail.html', context=context)

def favoris(request):
  favoris = Favoris.objects.filter(user=request.user)
  context = {
    'favoris': favoris,
  }
  return render(request, 'favoris.html', context=context)

def category(request):
  categories = Categorie.objects.all()
  return render(request, 'category.html', {'categories': categories})

def events_by_category(request, category_id):
  categorie = Categorie.objects.get(pk=category_id)
  events = Event.objects.filter(category=categorie, is_sold_out=False)
  return render(request, 'events_by_category.html', {'events': events, 'categorie': categorie})