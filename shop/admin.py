from django.contrib import admin
from shop.models import Category, Product, Article
from django.db import transaction

class CategoryAdmin(admin.ModelAdmin):

    list_display = ('name', 'active')


class ProductAdmin(admin.ModelAdmin):

    list_display = ('name', 'category', 'active')
    @transaction.atomic
    def disable_p(self, request, queryset):
        for product in queryset:
            if product.active is True:
                product.active = False
                product.save()
                product.articles.update(active=False)

    @transaction.atomic
    def enable_p(self, request, queryset):
        for product in queryset:
            if product.active is False:
                product.active = True
                product.save()



    actions = [disable_p, enable_p]

class ArticleAdmin(admin.ModelAdmin):

    list_display = ('name', 'product', 'category', 'active')

    @admin.display(description='Category')
    def category(self, obj):
        return obj.product.category


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Article, ArticleAdmin)
