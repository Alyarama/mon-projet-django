from django.urls import path
from .views import *



urlpatterns = [
    path('login/',connecter_compte, name='login'),
    path('creation/',creation_compte, name='creation'),
    path('deconnection/',Deconnection, name='deconnection'),
    path('verification/',Verification_mail, name='verification'),
    path('modification-code/<str:email>',changement_code, name='modifierCode'),
    
]
