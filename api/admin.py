from django.contrib import admin
from .models import CustomUser, Supermarket, Category, GroupProduct, Product, ProductPrice, ShoppingList, ListItem, UserBudget, BudgetCategory, BudgetExpense, BudgetAlert

# Custom admin for CustomUser
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'profile_image', 'address', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')

# Custom admin for Product to show more details
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'groupproduct', 'supermarket', 'category')
    list_filter = ('supermarket', 'category')
    search_fields = ('product_name', 'sku')

# Custom admin for ProductPrice to make it easy to see price changes
class ProductPriceAdmin(admin.ModelAdmin):
    list_display = ('product', 'rrp_price', 'sale_price', 'loyalty_card_price', 'datetime_price_updated')
    list_filter = ('datetime_price_updated',)
    search_fields = ('product__product_name',)

# Custom admin for ShoppingList to enhance user experience
class ShoppingListAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'creation_date')
    list_filter = ('creation_date',)
    search_fields = ('name', 'user__email')

class SupermarketAdmin(admin.ModelAdmin):
    list_display = ('supermarket_name', 'supermarket_url')
    search_fields = ('supermarket_name',)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'supermarket')
    list_filter = ('supermarket', 'parent')
    search_fields = ('name', 'supermarket__supermarket_name', 'parent__name')

class GroupProductAdmin(admin.ModelAdmin):
    list_display = ('common_product_name',)
    search_fields = ('common_product_name',)

class ListItemAdmin(admin.ModelAdmin):
    list_display = ('shoppinglist', 'product', 'quantity', 'datetime_added')
    list_filter = ('shoppinglist', 'datetime_added')
    search_fields = ('shoppinglist__name', 'product__product_name')

class UserBudgetAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'total_budget', 'start_date', 'end_date', 'creation_date', 'last_modified')
    list_filter = ('user', 'start_date', 'end_date', 'creation_date')
    search_fields = ('name', 'user__email')

class BudgetCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class BudgetExpenseAdmin(admin.ModelAdmin):
    list_display = ('userbudget', 'budgetcategory', 'product', 'amount_spent', 'expense_date')
    list_filter = ('userbudget', 'budgetcategory', 'expense_date')
    search_fields = ('userbudget__name', 'budgetcategory__name', 'product__product_name')

class BudgetAlertAdmin(admin.ModelAdmin):
    list_display = ('userbudget', 'alert_type', 'alert_date', 'message')
    list_filter = ('userbudget', 'alert_type', 'alert_date')
    search_fields = ('userbudget__name', 'message')


# Register your models here.
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Supermarket, SupermarketAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(GroupProduct, GroupProductAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductPrice, ProductPriceAdmin)
admin.site.register(ShoppingList, ShoppingListAdmin)
admin.site.register(ListItem, ListItemAdmin)
admin.site.register(UserBudget, UserBudgetAdmin)
admin.site.register(BudgetCategory, BudgetCategoryAdmin)
admin.site.register(BudgetExpense, BudgetExpenseAdmin)
admin.site.register(BudgetAlert, BudgetAlertAdmin)
