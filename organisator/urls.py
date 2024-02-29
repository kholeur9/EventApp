from django.urls import path
from .views import etape_1, secure_compte, register_organisation, connexion, deconnexion, dashboard

app_name = 'organisator'

urlpatterns = [
  path('', etape_1, name="etape-1"),
  path('secure-compte/', secure_compte, name="secure-compte"),
  path('register-organisation/', register_organisation, name="register-organisation"),
  path('connexion/', connexion, name="connexion"),
  path('dashboard/<uuid:organisatorID>/', dashboard, name="dashboard"),
  path('deconnexion/', deconnexion, name="deconnexion"),
]