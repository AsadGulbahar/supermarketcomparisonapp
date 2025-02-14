from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class CustomUser(AbstractUser):
    # Dont have to add username coz it's already part of AbstractUser
    email = models.EmailField('Email Address', unique=True)
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    address = models.TextField('Address', blank=True, null=True)


    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

#---------------------------------------------------------------------------------------------------------------------------------#

# Supermarket Model
class Supermarket(models.Model):
    supermarket_name = models.CharField(max_length=255)
    supermarket_url = models.URLField(null=True, blank=True)  
    supermarket_image = models.ImageField(upload_to='supermarket_images/', null=True, blank=True)

# Category Model
class Category(models.Model):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    supermarket = models.ForeignKey(Supermarket, on_delete=models.CASCADE, related_name='categories')

    class Meta:
        unique_together = ('name', 'supermarket',)  # Makes sure supermarket name is unique

    def __str__(self):
        return self.name
        

# GroupProduct Model
class GroupProduct(models.Model):
    common_product_name = models.CharField(max_length=255)

# Product Model
class Product(models.Model):
    groupproduct = models.ForeignKey(GroupProduct, on_delete=models.CASCADE, related_name='products', null=True, blank=True)
    product_name = models.CharField(max_length=255)
    product_weight = models.CharField(max_length=255)
    product_image_url = models.ImageField(upload_to='product_image/', null=True, blank=True)
    product_url = models.URLField()
    sku = models.CharField(max_length=255, null=True, blank=True)
    supermarket = models.ForeignKey('Supermarket', on_delete=models.CASCADE, related_name='products')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', null = True, blank=True)

  
# ProductPrice Model
class ProductPrice(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rrp_price = models.DecimalField(max_digits=10, decimal_places=2)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    loyalty_card_price = models.DecimalField(max_digits=10, decimal_places=2,  null=True, blank=True)
    sale_deal = models.CharField(max_length=255, null=True, blank=True)
    loyalty_card_deal = models.CharField(max_length=255, null=True, blank=True)
    rrp_price_per_weight = models.CharField(max_length=255, null=True, blank=True)
    datetime_price_updated = models.DateTimeField(auto_now=True)

#---------------------------------------------------------------------------------------------------------------------------------#

# ShoppingList Model
class ShoppingList(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    creation_date = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
                                         
# ListItem Model
class ListItem(models.Model):
    shoppinglist = models.ForeignKey(ShoppingList, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    datetime_added = models.DateTimeField(auto_now_add=True)

# UserBudget Model
class UserBudget(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    total_budget = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()
    creation_date = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)  # Automatically updates on model save

# BudgetCategory Model
class BudgetCategory(models.Model):
    name = models.CharField(max_length=255)

# BudgetExpense Model
class BudgetExpense(models.Model):
    userbudget = models.ForeignKey(UserBudget, on_delete=models.CASCADE)
    budgetcategory = models.ForeignKey(BudgetCategory, on_delete=models.CASCADE)
    product= models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    amount_spent = models.DecimalField(max_digits=10, decimal_places=2)
    expense_date = models.DateField()

# BudgetAlert Model
class BudgetAlert(models.Model):
    userbudget = models.ForeignKey(UserBudget, on_delete=models.CASCADE)
    alert_type = models.CharField(max_length=100)
    alert_date = models.DateField()
    message = models.TextField()

# Order Model
class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='orders')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


# OrderItem Model
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField(default=1)
    price_at_purchase = models.DecimalField(max_digits=10, decimal_places=2)

# ShippingAddress Model  
class ShippingAddress(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='shipping_address')
    address = models.TextField()
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)

    def __str__(self):
        return f"Shipping Address for Order {self.order.id}"













# User Model (Extending Django's built-in User model)

# class User(AbstractUser):
#     groups = models.ManyToManyField(
#         'auth.Group',
#         related_name='custom_user_groups',
#         blank=True
#     )
#     user_permissions = models.ManyToManyField(
#         'auth.Permission',
#         related_name='custom_user_permissions',
#         blank=True
#     )
