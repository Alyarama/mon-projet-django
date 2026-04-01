import re

from django.shortcuts import render,redirect

from django.contrib.auth import login,authenticate,logout
from django.contrib import messages
from django.core.validators import validate_email
from django.contrib.auth.models import User
# foction pour login

def connecter_compte(request):
    if request.method=='POST':
        
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('acc')
        else:
            messages.error(request,'Nom utilisateur ou mot de pass est incorrecte')
            return redirect('login')
    return render(request, 'login.html')
# fonction pour crée un compte

def creation_compte(request):
    if request.method=='POST':
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        password_confirm=request.POST['password_confirm']
        
        if password != password_confirm:
            messages.error(request, "les mots de passe ne sont pas identique.veuillez réessayer")
            return redirect("creation")

            
        if len(password) < 8 or not re.search(r'[A-Za-z]', password) or not re.search(r'[0-9]', password) or not re.search(r'[!@#$%(),.?{}|]', password):
            messages.error(request, 'Le mot de passe doit contenu au moins 8 chiffre incluant des lettre,des chiffre et des caractere ')
            return redirect("creation")
        
        try:
            validate_email(email)
        except ValueError:
            messages.error(request,"l'adresse e-mail invalid,veuillez réessayez. ")
            return redirect("creation")
        
        if User.objects.filter(username=username).exists():
            messages.error(request, "ce compte d'utilisateur existe dejà")
            return redirect("creation")
        if User.objects.filter(email=email).exists():
            messages.error(request,"Cette adresse email est utiliser dejà")
            return redirect("creation")
        
        User.objects.create_user(username=username,email=email, password=password)
        messages.error(request,"compte crée avec succes.connecte vous maintenant")
        return redirect("login")
    return render(request, 'creation.html')

#  fonction pour la verification de mot de passe 

def Verification_mail(request):
    if request.method=='POST':
        email=request.POST.get('email')
        
        # verification si l'email
        
        if not email:
            messages.error(request,"Veuillez rentre une adresse email valide.")
            return (request,'verificationMail.html')
        
        user=User.objects.filter(email=email).first
        if user:
            return redirect("modifierCode", email)
        
        else:
            messages.error(request,"cette adresse ne correspond à aucun compte. Veuillez réessaye avec un autre compte")
            return redirect('verification')
        
    return render(request, 'verificationMail.html')

# fonction pour changer le mot de passe apres verification

def changement_code(request,email):
    try:
        user=User.objects.get(email=email)
    except User.DoesNotExist:
        messages.error(request,"l'utilisateur introuvable")
        return redirect("login")
    
    if request.method=='POST':
        password=request.POST.get('password')
        password_confirm=request.POST.get('password_confirm')
        
        if password==password_confirm:
            if len(password) < 8 :
                messages.error(request,"le mot de passe doit contenue au mons 8 caracter")
            elif not any(char.isdigit() for char in password):
                messages.error(request,"le mot de passe doit contenu au moins un chiffre")
                
            elif not any(char.isalpha() for char in password):
                messages.error(request, "le mot de passe doit contenu au moins une lettre")
                
            else:
                user.set_password(password)
                user.save()
                messages.success(request,"Le mot de passe à bien été modifié. Connectez-vous maintenant")
                
                return redirect("login")
            
        else:
            messages.error(request,"Les mots de passe ne correspond pas. Réessayez")
            
            
    context ={
        'email':email
    }
    return render(request,"nouveauMDP.html",context)
        
   
        
              

    

# deconnecté

def Deconnection(request):
    logout(request)
    return redirect('login')
    
