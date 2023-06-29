from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import redirect,render
from shop.models import Category,Product,Article
from rest_framework.viewsets import ModelViewSet,ReadOnlyModelViewSet
from shop.serializers import CategoryListSerializer,CategoryDetailSerializer,ProductListSerializer,ProductDetailSerializer,ArticleListSerializer,ArticleDetailSerializer
from django.db import transaction
from rest_framework.decorators import action
from rest_framework.response import Response


class MultipleSerializerMixin:
    # Un mixin est une classe qui ne fonctionne pas de façon autonome
    # Elle permet d'ajouter des fonctionnalités aux classes qui les étendent

    detail_serializer_class = None

    def get_serializer_class(self):
        # Notre mixin détermine quel serializer à utiliser
        # même si elle ne sait pas ce que c'est ni comment l'utiliser
        if self.action == 'retrieve' and self.detail_serializer_class is not None:
            # Si l'action demandée est le détail alors nous retournons le serializer de détail
            return self.detail_serializer_class
        return super().get_serializer_class()
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

class CategoryViewset(MultipleSerializerMixin,ReadOnlyModelViewSet):

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
    @action(detail=True, methods=['post'])
    def disable(self, request, pk):
        # Nous pouvons maintenant simplement appeler la méthode disable
        self.get_object().disable()
        return Response()
class ProductViewset(ReadOnlyModelViewSet):

    serializer_class = ProductListSerializer
    detail_serializer_class = ProductDetailSerializer

    def get_queryset(self):
        return Product.objects.filter(active=True)
    def get_serializer_class(self):
    # Si l'action demandée est retrieve nous retournons le serializer de détail
        if self.action == 'retrieve':
            return self.detail_serializer_class
        return super().get_serializer_class()
    @action(detail=True, methods=['post'])
    def disable(self, request, pk):
        # Nous pouvons maintenant simplement appeler la méthode disable
        self.get_object().disable()
        return Response()
class AdminCategoryViewset(MultipleSerializerMixin, ModelViewSet):

    serializer_class = CategoryListSerializer
    detail_serializer_class = CategoryDetailSerializer

    def get_queryset(self):
        return Category.objects.all()
class ArticleViewset(ReadOnlyModelViewSet):
    serializer_class = ArticleListSerializer
    detail_serializer_class = ArticleDetailSerializer
    def get_queryset(self):
        queryset = Article.objects.filter(active=True)
        # Vérifions la présence du paramètre ‘category_id’ dans l’url et si oui alors appliquons notre filtre
        product_id = self.request.GET.get('product_id')
        if product_id is not None:
            queryset = queryset.filter(product_id=product_id)
        return queryset
class AdminCategoryViewset(MultipleSerializerMixin, ModelViewSet):

    serializer_class = CategoryListSerializer
    detail_serializer_class = CategoryDetailSerializer

    def get_queryset(self):
        return Category.objects.all()
class AdminArticleViewset(MultipleSerializerMixin, ModelViewSet):
    serializer_class = ArticleListSerializer
    detail_serializer_class = ArticleDetailSerializer
    def get_queryset(self):
        return Article.objects.all()


def test(request):
    return render(request,"test.html")
