from rest_framework.serializers import ModelSerializer

from shop.models import Category,Product

class CategorySerializer(ModelSerializer):

    class Meta:
        model = Category
        fields = ['id', 'name']
class ProductSerializer(ModelSerializer):

    class Meta:
        model = Product
        fields = ['name', 'description', 'active', 'date_created','date_updated','category']