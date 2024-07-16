from django.urls import path
from .views import getNetwork, getNetworkKamada, getRandomCsv

urlpatterns = [
    path('getNetwork', getNetwork.as_view(), name = 'getNetwork'),
    path('getNetworkKamada', getNetworkKamada.as_view(), name = 'getNetworkKamada'),
    path('getRandomCsv', getRandomCsv.as_view(), name = 'getRandomCsv'),
]