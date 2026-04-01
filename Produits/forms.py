from django.forms import ModelForm
from .models import Produits, Categories, Vente
from django import forms

class AjoutProduit(ModelForm):
    
    class Meta:
        model=Produits
        fields=[
            'name','category','price','quantite','description','date_expiration'
,'image'
]

widgets={
    'name':forms.TextInput(
        attrs={
            'placeholder': 'Entre le nom du produit',
            'class':'form_control'
        }
    ),
    'category':forms.Select(
        attrs={
            'class':'form-control'
        }
    ),
    'price':forms.NumberInput(
        attrs={
            'placeholder':'Entre le prix du produit',
            'class':'form-control'
        }
    ),
    'quantite':forms.NumberInput(
        attrs={
            'placeholder':'Entre la quantite du produit',
            'class':'form-control'
        }
    ),
    'description':forms.Textarea(
        attrs={
            'placeholder':'Entre la description',
            'class':'form-control',
            'rows':4
        }
    ),
    'date_expiration':forms.DateInput(
        attrs={
            'placeholder':'Date d\'expiration',
            'class':'form-control',
            'type':'date',

        }
    ),
    'image':forms.FileInput(
        attrs={
            'class':'form-control-file'
        }
    )
    
}

def __init__(self,*args,**kwargs):
    
    super(AjoutProduit,self).__init__(*args,**kwargs)
    
    self.fields['name'].error_messages={
        'required':'Le nom est obligatoire',
        'invalid':'Veuilez renseigner le nom'
    }
    
    self.fields['category'].error_messages={
        'required':'La categorie est obligatoire',
        'invalid':'Veuillez selectionne une categorie'
    }
    self.fields['price'].error_messages={
        'required':'Le prix est obligatoire',
        'invalid':'Veuillez entrez le prix valide'
    }
    self.fields['quantite'].error_messages={
        'required':'La quantite est obligatoire',
        'invalid':'Veuillez entrez la quantite'
    }
    self.fields['description'].error_messages={
        'required':'La description est obligatoire',
        'invalid':'Veuillez entrez la description'
    }
    self.fields['date_expiration'].error_messages={
        'required':'La date est obligatoire',
        'invalid':'Veuillez entrez la description'
    }
    
    # formulaire pour le vente
    
class AjoutVente(forms.ModelForm):
        
        quantite=forms.IntegerField(
            help_text='Veuillez entrez la quantité du produit',
            required=True,
            
        )
        customer=forms.CharField(
            help_text='Veuillez entrez le nom du client',
            required=True,
            max_length=100          
            
        )
        class Meta:
            model = Vente
            fields= ['quantite','customer']
            
            widgets= {
                'quantite':forms.TextInput(
                    attrs={
                        'placeholder':"Entrez la quantite",
                    'class': 'forms-control'
                    }
                ),          
                'customer':forms.TextInput(
                    attrs={
                        'placeholder':"Le nom du client",
                    'class': 'forms-control'
                    }
                )           
            }
            
            
        
  