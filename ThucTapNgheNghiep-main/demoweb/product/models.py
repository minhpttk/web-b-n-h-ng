from django.db import models
from order.models import Users
from django.utils.html import mark_safe

class Category(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="media", null=True, blank=True)

    def __str__(self):
        return self.name

    def image_tag(self):
        return mark_safe('<img src="%s" width="100px" height="100px" />'%(self.image.url))
    image_tag.short_description = 'Image'

class Product(models.Model):
    category = models.ForeignKey(
        Category, related_name="products", on_delete=models.CASCADE
    )
    title = models.CharField(max_length=100)
    cost = models.PositiveIntegerField(null=True, blank=True)
    quantity = models.PositiveIntegerField(null=True, blank=True)
    discount = models.PositiveIntegerField(null=True, blank=True)
    image = models.ImageField(upload_to="media", null=True, blank=True)
    author = models.CharField(max_length=50, null=True, blank=True)
    pages = models.PositiveIntegerField(null=True, blank=True)
    publisher = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def discount_cost(self):
        return round(self.cost * (1 - (self.discount / 100)))

    def rating(self):
        s = 0
        if self.product_review.all().count() > 0:
            for i in self.product_review.all():
                s += i.rating
            return round(s / self.product_review.all().count(), 1)
        else:
            return s

    def image_tag(self):
        return mark_safe('<img src="%s" width="100px" height="100px" />'%(self.image.url))
    image_tag.short_description = 'Image'

class Review(models.Model):
    user = models.ForeignKey(
        Users,
        related_name="user_review",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    product = models.ForeignKey(
        Product,
        related_name="product_review",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    created_time = models.DateTimeField(null=True, blank=True)
    review = models.TextField()
    rating = models.IntegerField()
