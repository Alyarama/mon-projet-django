from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("",Acc, name='acc'),
    path('produit/',affichage,name='home'),
    path('ajout/',AjoutProduits.as_view(),name='ajout'),
    # path('modification/<int:id>',modifier,name='modification'),
    path('modification/<int:pk>',update_donnees.as_view(),name='modifier'),
    path('supprimer/<int:id>/',supprimer,name='supprimer'),
    # path('detail/<int:id>/',detail,name='detail'),
    path('detail/<int:pk>/',detail.as_view(),name='detail'),
    path('recherche/',recherche,name='recherche'),
    path('ajoutvente/<int:id>/',VenteProduits,name='ajoutvente'),
    path('enregistrement-recu/<int:id>/',Saverecu,name='saverecu'),
    path('facture/<int:id>/',Facture,name='facture'),
    # path('ajout/',ajout_donnees,name='ajout'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

