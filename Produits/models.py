from django.db import models

# Create your models here.
class Categories(models.Model):
    name=models.CharField(max_length=250)
    def __str__(self):
        return self.name
class Produits(models.Model):
    name=models.CharField(max_length=50)
    category=models.ForeignKey(Categories, on_delete=models.CASCADE)
    price=models.IntegerField()
    quantite=models.PositiveIntegerField(default=0)
    description=models.TextField()
    date_ajout=models.DateTimeField(auto_now_add=True)
    date_expiration=models.DateField()
    image=models.ImageField(null=True,blank=True,upload_to='produits/')
    
    class Meta:
        ordering=['-date_ajout']
        
    def statut_quantite(self):
        if self.quantite==0:
            return 'red'
        elif self.quantite<=10:
            return 'orange'
        else:
            return 'green'
    def __str__(self):
        return self.name

class Customer(models.Model):
    name=models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Vente(models.Model):
    produit=models.ForeignKey(Produits,on_delete=models.CASCADE)
    sale_date=models.DateTimeField(auto_now=True)
    quantite=models.PositiveIntegerField()
    customer=models.CharField(max_length=100)
    total_amont=models.DecimalField(max_digits=10,decimal_places=2)  
    
    def __str__(self):
        return self.produit
    
class Facture_Client(models.Model):
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE)
    quantite=models.PositiveIntegerField()
    date_achat=models.DateTimeField(auto_now_add=False) 
    total_amont=models.ForeignKey(Vente,on_delete=models.CASCADE)
    produit=models.ForeignKey(Produits,on_delete=models.CASCADE)
    
    def __str__(self):
       return f"Le recu de {self.customer.customer}"  
    
