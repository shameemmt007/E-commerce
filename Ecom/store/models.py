from django.db import models
# Create your models here.
from django.contrib.auth.models import User


class category(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField()
    image = models.ImageField(upload_to='category/')

    def __str__(self):
        return self.name

class Product(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    name = models.CharField(max_length=150)
    categorys = models.ForeignKey(category,on_delete=models.CASCADE,null=True)
    description = models.TextField()
    image = models.ImageField(null=True,upload_to='products/')
    price = models.FloatField()
    stock = models.IntegerField()

    def __str__(self):
        return self.name








# class Cart(models.Model):
#     user = models.OneToOneField(User,on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True,null=True)
#     updated_at = models.DateTimeField(auto_now_add=True,null=True)

#     # def total_price(self):
#     #     return sum(item.total_price for item in self.items.all())


# class CartItem(models.Model):
#     cart = models.ForeignKey(Cart, related_name="items",on_delete=models.CASCADE)
#     product = models.ForeignKey(Product,on_delete=models.CASCADE)
#     quantity = models.PositiveIntegerField(default=1)
#     added_at = models.DateTimeField(auto_now_add=True,null=True)

    # @property
    # def total_price(self):
    #     return self.product.price * self.quantity




class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    name = models.CharField()
    email = models.EmailField()
    
    bio = models.TextField()
    ppic = models.ImageField(upload_to='profile')



class Order(models.Model):
    STATUS_CHOICES = (
        ('PENDING','pending'),
        ('SHIPPED','shipped'),
        ('DELIVERED','delivered'),
    )
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    status = models.CharField(max_length=20,choices=STATUS_CHOICES,default='PENDING')

    def total_price(self):
        return sum(item.product.price * item.quantity for item in self.items.all())
    
    def __str__(self):
        return f"order{self.id} by {self.user.username}"
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE,related_name="items")
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1,null=True)

    def subtotal(self):
        return self.product.price * self.quantity


    def __str__(self):
        return f"{self.product.name} (x{self.quantity})"
    
    
