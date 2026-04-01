from django.contrib import messages
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.forms import ModelForm
from django.views.generic import ListView,CreateView,UpdateView,DetailView
from django.shortcuts import redirect, render,get_object_or_404
from django.core.files.storage import FileSystemStorage
from .models import *
from datetime import datetime
from .forms import AjoutProduit, AjoutVente
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='login')
def affichage(request):
    
    donnees=Produits.objects.all()
    
    context={
        'donnees':donnees
    }
    return render(request, 'Produits/home.html',context)

@login_required(login_url='login')
def Acc(request):
    return render(request, 'Produits/acc.html')
class AjoutProduits(LoginRequiredMixin, CreateView):
    # utilisation du modele
    model=Produits
    # specifier le formulaire à utiliser
    form_class=AjoutProduit
    #affichage du template
    template_name='Produits/ajout_donne.html'
    #redirection
    success_url=reverse_lazy('home')
    login_url='login'
class update_donnees(LoginRequiredMixin, UpdateView):
    model=Produits
    
    form_class=AjoutProduit
    template_name='Produits/modification.html'
    success_url=reverse_lazy('home')
    login_url='login'    
# fonction pour supprime
@login_required(login_url='login')
def supprimer(request, id):
    if request.method == "POST":
        produit = get_object_or_404(Produits, id=id)
        produit.delete()
        return JsonResponse({'success': True, 'message': "Produit supprimé avec succès"})
    
    return JsonResponse({'success': False, 'message': "Méthode non autorisée"}) 
# class pour les detail

class detail(LoginRequiredMixin, DetailView):
    model=Produits
    template_name='Produits/detail.html'
    context_object_name='n'
    login_url='Utilisateurs:login'    
# fonction de recherche produit
@login_required(login_url='login')
def recherche(request):
    query=request.GET.get('produit')
    donnees=Produits.objects.filter(name__icontains=query)
    context={
        'donnees':donnees
    }
 
    return render(request,'Produits/resultat_recherche.html',context)
 # fonction pour la vente
    
def VenteProduits(request, id):
     produit = get_object_or_404(Produits, id=id)
     message = None
        
     if request.method == 'POST':
            form= AjoutVente(request.POST)
            if form.is_valid():
                quantite = form.cleaned_data['quantite']
                customer = form.cleaned_data['customer']
                
                if quantite > produit.quantite:
                    message = 'La quantite demandée est supérieur à votre stock'
                    
                else:
                    customer,_=Customer.objects.get_or_create(name=customer)
                    
                    total_amont=produit.price * quantite
                    sale=Vente(produit=produit, quantite=quantite,total_amont=total_amont,customer=customer)
                    sale.save()
                    
                    produit.quantite-= quantite
                    produit.save()
                    return redirect('facture', id=sale.id)
     else:
         form=AjoutVente()
         
     if produit.quantite <= 5 and not message:
             message = 'Attention le stock est bas !'
             
     context={
            'produit':produit,
            'form':form,
            'message':message
        }
     return render(request,'Produits/formulaire-vente.html',context)
 # fonction pour recu
 
def Saverecu(request, id):
    vente = get_object_or_404(Vente,id=id)
    customer=vente.customer
    quantite=vente.quantite
    total_amont=vente.total_amont
    produit = vente.produit
    
    recu = Facture_Client(
        customer = customer,
        quantite = quantite,
        total_amont = total_amont,
        produit = produit
        
    )
    
    recu.save()
    return redirect('facture', id = id)

# fonction pour la facture
def Facture(request, id):
    sale = get_object_or_404(Vente, id=id)
    customer=sale.customer
    quantite=sale.quantite
    produit=sale.produit
    sale_date = sale.sale_date
    total_amont = sale.total_amont
    
    context = {
        'sale': sale,
        'customer': customer,
        'quantite': quantite,
        'produit':produit,
        'sale_date':sale_date,
        'id' : id,
        'prix_unitaire': produit.price,
        'total_amont':total_amont
    }
    return render(request, 'Produits/facture-client.html', context)  
                     
                     
                    

#fonction detail
# def detail(request, id):
#     n=Produits.objects.get(id=id)
#     return render( request, 'Produits/detail.html', {'n':n})
# def modifier(request, id):
#     produit = get_object_or_404(Produits, id=id)
#     categories = Categories.objects.all()
#     errors = {}

#     if request.method == 'POST':
#         name = request.POST.get('name')
#         category_id = request.POST.get('category')
#         price = request.POST.get('price')
#         quantite = request.POST.get('quantite')
#         description = request.POST.get('description')
#         date_expiration = request.POST.get('date_expiration')
#         image = request.FILES.get('image')

#         # ✅ Validation correcte
#         if not name:
#             errors['name'] = 'Le nom est requis'
#         if not category_id:
#             errors['category'] = 'La catégorie est requise'
#         if not price:
#             errors['price'] = 'Le prix est requis'
#         if not quantite:
#             errors['quantite'] = 'La quantité est requise'
#         if not description:
#             errors['description'] = 'La description est requise'

#         # ✅ Validation + conversion date
#         date_obj = None
#         if date_expiration:
#             try:
#                 date_obj = datetime.strptime(date_expiration, '%Y-%m-%d').date()
#             except ValueError:
#                 errors['date_expiration'] = "Format invalide (AAAA-MM-JJ)"

#         # ✅ Si pas d'erreurs
#         if not errors:
#             category = get_object_or_404(Categories, id=category_id)

#             produit.name = name
#             produit.category = category
#             produit.price = price
#             produit.quantite = quantite
#             produit.description = description
#             produit.date_expiration = date_obj

#             # ✅ Correction image (IMPORTANT)
#             if image:
#                 fs = FileSystemStorage()
#                 filename = fs.save(image.name, image)  # 🔥 correction ici
#                 produit.image = filename  # pas fs.url()

#             produit.save()

#             messages.success(request, "Produit modifié avec succès ✅")
#             return redirect("home")

#         # ✅ Afficher les erreurs
#         for error in errors.values():
#             messages.error(request, error)

#     return render(request, "Produits/modification.html", {
#         'produit': produit,
#         'categories': categories,
#         'errors': errors
#     })
# def ajout_donnees(request):
    
#     errors={}
#     if request.method=='POST':
#         name=request.POST['name']
#         price=request.POST['price']
#         quantite=request.POST['quantite']
#         description=request.POST['description']
#         date_expiration=request.POST['date_expiration']
#         image=request.FILES['image']
        
#         try:
#             date_expiration=datetime.strptime(date_expiration, '%Y-%m-%d')
#         except ValueError:
#             errors['date_expiration']="Le format de la date est n'est pas bon.Essaye ceci:AAAA-MM-JJ" 
            
#         try:
#             price=float(price) 
#             if price<0:
#                 errors['price']="le prix ne peut pas etre négatif" 
#         except ValueError:
#             errors['price']="Entrez un prix valide svp" 
#         if not errors:
#             try:
                             
#                 category=Categories.objects.get(pk=request.POST['category'])
#                 savedonnes=Produits(name=name, price=price ,quantite=quantite,description=description,date_expiration=date_expiration, image=image,category=category)
#                 savedonnes.save()
#                 messages.success(request, "✅ Produit ajouté avec succès")
#                 return redirect('home')
#             except Categories.DoesNotExist:
#                 errors['category']=f'la categorie specifie est introuvable.'
#             except KeyError as e:
#                 errors[str(e)]=f'Le champ {e} est manquant dans la requete.'
#             except Exception as e:
#                 messages.error(request, f'une erreur est survenue:{e} ')
#     category=Categories.objects.all()
    
#     return render(request, 'Produits/ajout_donne.html',{"category":category, "errors":errors})