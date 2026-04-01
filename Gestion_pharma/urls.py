
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Produits.urls')),
    path('', include('Utilisateurs.urls')),

]
