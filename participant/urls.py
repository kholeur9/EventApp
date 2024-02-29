from django.urls import path, include
from .views import register, secure_compte, login_view, logout_view, home_view, profile_user, informations

app_name = 'participant'

urlpatterns = [
  #path('google-authenticate/', google_authenticate, name='google_authenticate'),
  path('register/', register, name='register'),
  path('secure-compte/', secure_compte, name='secure-compte'),
  path('login/', login_view, name='login_view'),
  path('logout/', logout_view, name='logout'),
  path('', home_view, name='home_view'),
  path('profile-user/', profile_user, name='profile-user'),
  path('informations/<uuid:participant_id>/', informations, name='informations'),
]