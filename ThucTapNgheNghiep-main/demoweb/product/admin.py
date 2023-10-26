from django.contrib import admin
from .models import Category, Product, Review
from django.utils.html import mark_safe
from django.urls import reverse

# Register your models here.


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = [ "image_tag","name"]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["image_tag", "title", "category_link", "cost", "quantity", "discount","rating"]
    list_display_links = ["title", "category_link"]
    search_fields=["title","category__name"]
    list_filter = ["cost"]

    def category_link(self, obj):
        url = reverse("admin:product_category_change", args=[obj.category.id])
        link = '<a href="%s">%s</a>' % (url, obj.category.name)
        return mark_safe(link)
    category_link.short_description = 'Category'

    

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user','product','review','rating','created_time']
