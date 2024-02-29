from django.urls import path
from .views import favoris_add, detail_event, favoris, category

app_name = 'evenement'

urlpatterns = [
  path('<int:pk>/', detail_event, name='detail_event'),
  path('favoris/<int:pk>/', favoris_add, name='favoris_add'),
  path('favoris/', favoris, name='favoris'),
  path('category/', category, name='category'),
]