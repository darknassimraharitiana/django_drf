from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import redirect,render
from shop.models import Category,Product,Article
from rest_framework.viewsets import ModelViewSet,ReadOnlyModelViewSet
from shop.serializers import CategoryListSerializer,CategoryDetailSerializer,ProductSerializer,ArticleSerializer

class CategoryAPIView(APIView):

    def get(self, *args, **kwargs):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)
class ProductAPIView(APIView):

    def get(self, *args, **kwargs):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
##class CategoryViewset(ModelViewSet):
##
##    serializer_class = CategorySerializer
##
##    def get_queryset(self):
##        return Category.objects.all()
class CategoryViewset(ReadOnlyModelViewSet):

    serializer_class = CategoryListSerializer
    # Ajoutons un attribut de classe qui nous permet de définir notre serializer de détail
    detail_serializer_class = CategoryDetailSerializer

    def get_queryset(self):
        return Category.objects.filter(active=True)

    def get_serializer_class(self):
    # Si l'action demandée est retrieve nous retournons le serializer de détail
        if self.action == 'retrieve':
            return self.detail_serializer_class
        return super().get_serializer_class()
class ProductViewset(ReadOnlyModelViewSet):

    serializer_class = ProductSerializer

    def get_queryset(self):
        queryset = Product.objects.filter(active=True)
        # Vérifions la présence du paramètre ‘category_id’ dans l’url et si oui alors appliquons notre filtre
        category_id = self.request.GET.get('category_id')
        if category_id is not None:
            queryset = queryset.filter(category_id=category_id)
        return queryset
def test(request):
    return render(request,"test.html")
class ArticleViewset(ReadOnlyModelViewSet):
    serializer_class = ArticleSerializer

    def get_queryset(self):
        queryset = Article.objects.filter(active=True)
        # Vérifions la présence du paramètre ‘category_id’ dans l’url et si oui alors appliquons notre filtre
        product_id = self.request.GET.get('product_id')
        if product_id is not None:
            queryset = queryset.filter(product_id=product_id)
        return queryset
