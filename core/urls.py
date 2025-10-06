from django.urls import path
from .views import home, bpo, explore, market, why, it_visa, contact_view

urlpatterns = [
    path('', home, name='home'),
    path('bpo/', bpo, name='bpo'),
    path('explore/', explore, name='explore'),
    path('market/', market, name='market'),
    path('why/', why, name='why'),
    path('it-visa/', it_visa, name='it-visa'),
    path('contact/', contact_view, name='contact'),
]
