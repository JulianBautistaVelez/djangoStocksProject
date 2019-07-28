from django.urls import path

from . import views

app_name = 'stocks'

urlpatterns = [
    path('crypto', views.crypto, name='crypto'),
    path('dow_jones_30', views.dow_jones_30, name='dow_jones_30'),
    path('company/<str:company>', views.company, name='company'),
    path('stock_exchange_company/<str:company>', views.stock_exchange_company,
         name='stock_exchange_company'),

]
