from django.urls import path
from .views import *

urlpatterns = [
    path('', login_, name='login_'),
    path('register/', register, name='register'),
    path('profile/', profile, name='profile'),
    path('profile/', profile, name='profile'),
    path('logout_/',logout_,name='logout_'),
    path('reset/',reset,name='reset'),
    path('update/',update,name='update'),
    path('forgot/',forgot,name='forgot'),
    path('new_pasw/',new_pasw,name='new_pasw')

]