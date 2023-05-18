from django.urls import path, include
from cliente.views import TestView, CreateCliente,GetCliente,EditCliente,DeleteCliente


urlpatterns = [
    path('test/', TestView.as_view(), name='test'),
    path('create/', CreateCliente.as_view(), name='create'),
    path('get/', GetCliente.as_view(), name='get'),
    path('edit/', EditCliente.as_view(), name='edit'),
    path('delete/', DeleteCliente.as_view(), name='delete'),
    
]