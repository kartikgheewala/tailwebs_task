from django.urls import path
from .views import *

urlpatterns = [
    path('', login, name='login'),
    path('logout', logout, name='logout'),
    path('dashboard', dashboard, name='dashboard'),
]
