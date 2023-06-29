from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from shop.models import Category,Product,Article





class ArticleListSerializer(ModelSerializer):
    class Meta:
        model = Article
        fields = ['id','name','product', 'description', 'active','price', 'date_created','date_updated',]
    def validate_price(self, value):
        # Nous vérifions que la catégorie existe
        if value<1:
        # En cas d'erreur, DRF nous met à disposition l'exception ValidationError
            raise serializers.ValidationError('price must over 1')
        return value
    def validate(self,data):
        if Product.objects.get(name=data['product']).active==False:
        # Levons une ValidationError si ça n'est pas le cas
            raise serializers.ValidationError('product must active')
        return data
class ProductDetailSerializer(ModelSerializer):
    articles = serializers.SerializerMethodField()
    class Meta:
        model = Product
        fields = ['id','name', 'category', 'date_created','date_updated','articles']
    def get_articles(self, instance):
        # Le paramètre 'instance' est l'instance de la catégorie consultée.
        # Dans le cas d'une liste, cette méthode est appelée autant de fois qu'il y a
        # d'entités dans la liste

        # On applique le filtre sur notre queryset pour n'avoir que les produits actifs
        queryset = instance.articles.filter(active=True)
        # Le serializer est créé avec le queryset défini et toujours défini en tant que many=True
        serializer = ArticleListSerializer(queryset, many=True)
        # la propriété '.data' est le rendu de notre serializer que nous retournons ici
        return serializer.data
class ProductListSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ['id','name', 'date_created','date_updated', 'category','ecoscore',]
class ArticleDetailSerializer(ModelSerializer):
    products = serializers.SerializerMethodField()
    class Meta:
        model = Article
        fields = ['id','name', 'description', 'active','price', 'date_created','date_updated','products']
    def get_products(self, instance):
        # Le paramètre 'instance' est l'instance de la catégorie consultée.
        # Dans le cas d'une liste, cette méthode est appelée autant de fois qu'il y a
        # d'entités dans la liste

        # On applique le filtre sur notre queryset pour n'avoir que les produits actifs
        queryset = instance.product.filter(active=True)
        # Le serializer est créé avec le queryset défini et toujours défini en tant que many=True
        serializer = ProductSerializer(queryset, many=True)
        # la propriété '.data' est le rendu de notre serializer que nous retournons ici
        return serializer.data
class CategoryListSerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name','date_created','date_updated']
    def validate_name(self, value):
        # Nous vérifions que la catégorie existe
        if Category.objects.filter(name=value).exists():
        # En cas d'erreur, DRF nous met à disposition l'exception ValidationError
            raise serializers.ValidationError('Category already exists')
        return value
    def validate(self, data):
        # Effectuons le contrôle sur la présence du nom dans la description
        if data['name'] not in data['description']:
        # Levons une ValidationError si ça n'est pas le cas
            raise serializers.ValidationError('Name must be in description')
        return data
class CategoryDetailSerializer(ModelSerializer):
##    products = ProductSerializer(many=True)
    products = serializers.SerializerMethodField()
    class Meta:
        model = Category
        fields = ['id', 'name','date_created','date_updated','products']
    def get_products(self, instance):
        # Le paramètre 'instance' est l'instance de la catégorie consultée.
        # Dans le cas d'une liste, cette méthode est appelée autant de fois qu'il y a
        # d'entités dans la liste

        # On applique le filtre sur notre queryset pour n'avoir que les produits actifs
        queryset = instance.products.filter(active=True)
        # Le serializer est créé avec le queryset défini et toujours défini en tant que many=True
        serializer = ProductListSerializer(queryset, many=True)
        # la propriété '.data' est le rendu de notre serializer que nous retournons ici
        return serializer.data