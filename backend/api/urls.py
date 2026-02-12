from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup),
    path('login/', views.login_view),
    path('profile/', views.user_profile),
]