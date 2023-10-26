from django.db import models
from django.contrib.auth.models import AbstractUser
from vi_address.models import City, District, Ward

# from product.models import Product
# from django.apps import apps
# Product = apps.get_model('product', 'Product')
# Create your models here.


class Users(AbstractUser):
    QUESTION_CHOICE = (
        ("1", "Cuốn sách yêu thích nhất của bạn?"),
        ("2", "Cuốn sách đầu tiên bạn đọc?"),
        ("3", "Loài động vật bản yêu thích nhất?"),
        
    )
    
    question = models.CharField(choices=QUESTION_CHOICE,default="1",max_length=255)
    answer = models.CharField(max_length=255, blank=True,null=True)
    phone = models.CharField(max_length=10,null=True, blank=True)
    city = models.ForeignKey(City,on_delete=models.CASCADE, null=True, blank=True)
    district = models.ForeignKey(District,on_delete=models.CASCADE, null=True, blank=True)
    ward = models.ForeignKey(Ward,on_delete=models.CASCADE, null=True, blank=True)
    street = models.CharField(max_length=100,null=True, blank=True)
    avatar = models.ImageField(upload_to='media', null=True, blank=True)
    
    class Meta:
        db_table = "auth_user"

    def show_avt(self):
        if self.avatar:
            return self.avatar.url
        else:
            return ""


class Order(models.Model):
    status_choices = (
        (1, "Cart"),
        (2, "Ordered"),
        (3, "Cancelled"),
    )

    total_price = models.PositiveIntegerField(default=0)
    quantity = models.PositiveIntegerField(default=0)
    user = models.ForeignKey(
        Users, related_name="users", on_delete=models.CASCADE, null=True, blank=True
    )
    status = models.IntegerField(choices=status_choices, default=1)
    datetime = models.DateTimeField(null=True, blank=True)


class Order_detail(models.Model):
    order = models.ForeignKey(Order, related_name="order", on_delete=models.CASCADE)
    product = models.ForeignKey(
        "product.Product", related_name="product_pr", on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField(default=1)

    def total(sefl):
        return sefl.quantity * sefl.product.discount_cost()


class Contact(models.Model):
    name = models.CharField(max_length=255)
    number = models.IntegerField(default=0)
    email = models.EmailField(max_length=25)
    message = models.TextField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
