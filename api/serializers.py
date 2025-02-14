# serializers.py
from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Product, ProductPrice, Supermarket, GroupProduct, ShoppingList, ListItem, Category

User = get_user_model()

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'profile_image', 'address', 'password']
        extra_kwargs = {'password': {'write_only': True, 'required': False}}

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        profile_image = validated_data.get('profile_image', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        if password:
            instance.set_password(password)
        
        instance.save()
        return instance


# Serializer for ProductPrice
class ProductPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductPrice
        fields = ['rrp_price', 'sale_price', 'loyalty_card_price', 'sale_deal', 'loyalty_card_deal', 'rrp_price_per_weight', 'datetime_price_updated']

# Serializer for Supermarket
class SupermarketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supermarket
        fields = ['id', 'supermarket_name', 'supermarket_image']


class LatestProductPriceSerializer(serializers.ModelSerializer):
    """Serializer for the latest ProductPrice instance."""
    class Meta:
        model = ProductPrice
        fields = ['rrp_price', 'sale_price', 'loyalty_card_price', 'sale_deal', 'loyalty_card_deal', 'rrp_price_per_weight', 'datetime_price_updated']

class ProductSerializer(serializers.ModelSerializer):
    latest_price = serializers.SerializerMethodField()
    supermarket = SupermarketSerializer(read_only=True)  # Use the SupermarketSerializer here

    class Meta:
        model = Product
        fields = ['id', 'product_name', 'product_weight', 'product_image_url', 'product_url', 'sku', 'supermarket', 'latest_price']

    def get_latest_price(self, obj):
        latest_price = obj.productprice_set.order_by('-datetime_price_updated').first()
        return LatestProductPriceSerializer(latest_price).data if latest_price else None


class GroupProductSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True)  

    class Meta:
        model = GroupProduct
        fields = ['id', 'common_product_name', 'products']

class ShoppingListSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)
    
    class Meta:
        model = ShoppingList
        fields = ['id', 'name', 'products', 'creation_date', 'last_modified']
        read_only_fields = ['creation_date', 'last_modified']


class ListItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = ListItem
        fields = ['product', 'quantity']

class ProductPriceHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductPrice
        fields = ['rrp_price', 'sale_price', 'loyalty_card_price','sale_deal', 'loyalty_card_deal' ,'datetime_price_updated']