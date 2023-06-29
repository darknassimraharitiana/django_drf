from django.db import models
from django.db import transaction
from rest_framework.decorators import action
import requests

class Category(models.Model):

    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    @transaction.atomic
    def disable(self):
        if self.active is False:
        # Ne faisons rien si la catégorie est déjà désactivée
            return
        self.active = False
        self.save()
        self.products.update(active=False)


class Product(models.Model):

    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    active = models.BooleanField(default=False)

    category = models.ForeignKey('shop.Category', on_delete=models.CASCADE, related_name='products')

    def __str__(self):
        return self.name
    @transaction.atomic
    def disable(self):
        if self.active is False:
        # Ne faisons rien si la catégorie est déjà désactivée
            return
        self.active = False
        self.save()
        self.articles.update(active=False)
    @transaction.atomic
    def enable(self):
        if self.active is True:
        # Ne faisons rien si la catégorie est déjà désactivée
            return
        self.active = True
        self.save()
        self.articles.update(active=True)


    def call_external_api(self, method, url):
        # l'appel doit être le plus petit possible car appliquer un mock va réduire la couverture de tests
        # C'est cette méthode qui va être monkey patchée
        return requests.request(method, url)


    @property
    def ecoscore(self):
        # Nous réalisons l'appel à open food fact
        response = self.call_external_api('GET', 'https://world.openfoodfacts.org/api/v0/product/3229820787015.json')
        if response.status_code == 200:
        # et ne renvoyons l'écoscore que si la réponse est valide
            return response.json()['product']['ecoscore_grade']


class Article(models.Model):

    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    active = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=4, decimal_places=2)

    product = models.ForeignKey('shop.Product', on_delete=models.CASCADE, related_name='articles')

    def __str__(self):
        return self.name
