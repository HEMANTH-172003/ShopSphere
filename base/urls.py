from django.urls import path
from .views import *

urlpatterns = [
    path('home/',home,name='home'),
    path('addtocart/<int:pk>',addtocart,name='addtocart'),
    path('cart/',cart,name='cart'),
    path('remove/<int:pk>',remove,name='remove'),
    path('add/<int:pk>',add,name='add'),
    path('sub/<int:pk>',sub,name='sub')
]