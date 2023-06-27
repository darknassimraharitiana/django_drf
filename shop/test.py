from django.urls import reverse_lazy,reverse
from rest_framework.test import APITestCase

from shop.models import Category,Product
##
##class TestCategory(APITestCase):
##    # Nous stockons l’url de l'endpoint dans un attribut de classe pour pouvoir l’utiliser plus facilement dans chacun de nos tests
##    url = reverse_lazy('category-list')
##
##    def format_datetime(self, value):
##        # Cette méthode est un helper permettant de formater une date en chaine de caractères sous le même format que celui de l’api
##        return value.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
##
##    def test_list(self):
##        # Créons deux catégories dont une seule est active
##        category = Category.objects.create(name='Fruits', active=True)
##        Category.objects.create(name='Légumes', active=False)
##
##        # On réalise l’appel en GET en utilisant le client de la classe de test
##        response = self.client.get(self.url)
##        # Nous vérifions que le status code est bien 200
##        # et que les valeurs retournées sont bien celles attendues
##        self.assertEqual(response.status_code, 200)
##        excepted = [
##            {
##                'id': category.pk,
##                'name': category.name,
##                'date_created': self.format_datetime(category.date_created),
##                'date_updated': self.format_datetime(category.date_updated),
##            }
##        ]
##        self.assertEqual(excepted, response.json())
##
##    def test_create(self):
##        # Nous vérifions qu’aucune catégorie n'existe avant de tenter d’en créer une
##        self.assertFalse(Category.objects.exists())
##        response = self.client.post(self.url, data={'name': 'Nouvelle catégorie'})
##        # Vérifions que le status code est bien en erreur et nous empêche de créer une catégorie
##        self.assertEqual(response.status_code, 405)
##        # Enfin, vérifions qu'aucune nouvelle catégorie n’a été créée malgré le status code 405
##        self.assertFalse(Category.objects.exists())
class ShopAPITestCase(APITestCase):
    # Nous stockons l’url de l'endpoint dans un attribut de classe pour pouvoir l’utiliser plus facilement dans chacun de nos tests
    url = reverse_lazy('product-list')

    def format_datetime(self, value):
        # Cette méthode est un helper permettant de formater une date en chaine de caractères sous le même format que celui de l’api
        return value.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

    def test_list(self):
        # Créons deux catégories dont une seule est active
        category1 = Category.objects.create(name='epice', active=False)
        self.category=category1
        category2 = Category.objects.create(name='legume', active=False)

        product1 = Product.objects.create(name='sucre', category=category1, active=True)
        product2 = Product.objects.create(name='sel', category=category2, active=True)

        # On réalise l’appel en GET en utilisant le client de la classe de test
        response = self.client.get(self.url)

        # Nous vérifions que le status code est bien 200
        # et que les valeurs retournées sont bien celles attendues
        self.assertEqual(response.status_code, 200)

        expected = [
            {
                'id': product1.pk,
                'name': product1.name,
                'category': category1.id,
                'date_created': self.format_datetime(product1.date_created),
                'date_updated': self.format_datetime(product1.date_updated),


            },
            {
                'id': product2.pk,
                'name': product2.name,
                'category': category2.id,
                'date_created': self.format_datetime(product2.date_created),
                'date_updated': self.format_datetime(product2.date_updated),

            }
        ]

        self.assertEqual(expected, response.json())

    def test_create(self):
        # Nous vérifions qu’aucune catégorie n'existe avant de tenter d’en créer une
        self.assertFalse(Product.objects.exists())
        response = self.client.post(self.url, data={'name': 'Nouvelle produits'})
        # Vérifions que le status code est bien en erreur et nous empêche de créer une catégorie
        self.assertEqual(response.status_code, 405)
        # Enfin, vérifions qu'aucune nouvelle catégorie n’a été créée malgré le status code 405
        self.assertFalse(Product.objects.exists())
class TestCategory(ShopAPITestCase):
    def test_detail(self):
        # Nous utilisons l'url de détail
        url_detail = reverse('category-detail',kwargs={'pk': self.category.pk})
        response = self.client.get(url_detail)
        # Nous vérifions également le status code de retour ainsi que les données reçues
        self.assertEqual(response.status_code, 200)
        excepted = {
            'id': self.category.pk,
            'name': self.category.name,
            'date_created': self.format_datetime(self.category.date_created),
            'date_updated': self.format_datetime(self.category.date_updated),
            'products': self.get_product_detail_data(self.category.products.filter(active=True)),
        }
        self.assertEqual(excepted, response.json())