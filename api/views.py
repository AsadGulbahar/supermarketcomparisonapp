from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from .models import CustomUser, Supermarket, Category, GroupProduct, Product, ProductPrice
from .models import ShoppingList, ListItem
from .models import Order, OrderItem
from .models import UserBudget, BudgetCategory, BudgetExpense, BudgetAlert

@login_required
def main_spa(request: HttpRequest) -> HttpResponse:
    return render(request, 'api/spa/index.html', {})

# SIGNUP LOGIN & LOGOUT BELOW
def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()  # Save the new user
            login(request, user)  # Log the user in
            # Redirect to a login page
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'api/spa/signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)  # Log the user in
                # Redirect to a success page
                return redirect('index')
            else:
                # Return an 'invalid login' error message
                return render(request, 'api/spa/login.html', {'form': form, 'error_message': 'Invalid username or password.'})
    else:
        form = CustomAuthenticationForm()
    return render(request, 'api/spa/login.html', {'form': form})

@login_required
def logout_view(request):
    auth.logout(request)
    return redirect('login')


from rest_framework import generics, permissions
from .serializers import CustomUserSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        # Returns the current user so a user can only access their own profile
        return self.request.user


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Product
from .serializers import ProductSerializer


class SearchResultsView(APIView):   
    def get(self, request, *args, **kwargs):
        query = request.query_params.get('query')
        supermarket_id = request.query_params.get('supermarket_id')

        if query is None:
            print("Query parameter is missing.")
            return Response({'error': 'Missing query parameter'}, status=status.HTTP_400_BAD_REQUEST)

        print(f"Query: {query}, Supermarket ID: {supermarket_id}")

        # Query for products in the chosen supermarket
        if supermarket_id:
            products = Product.objects.filter(product_name__icontains=query, supermarket_id=supermarket_id)
            print(f"Products found in specified supermarket: {products.count()}")

            # If no products found in the chosen supermarket, search in other supermarkets
            if not products.exists():
                products = Product.objects.filter(product_name__icontains=query).exclude(supermarket_id=supermarket_id)
                print("No products found in the specified supermarket, searching in other supermarkets...")
                print(f"Products found in other supermarkets: {products.count()}")
        else:
            products = Product.objects.filter(product_name__icontains=query)
            print(f"Products found (no specific supermarket): {products.count()}")

        serializer = ProductSerializer(products, many=True)
        serialized_data = serializer.data
        print(f"Serialized data: {serialized_data}")
        
        return Response(serialized_data)




from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Product, GroupProduct
from .serializers import GroupProductSerializer

class ProductGroupDetailView(APIView):
    """
    Retrieve GroupProduct along with all related Product entities and their details,
    based on the given Product ID.
    """

    def get(self, request, product_id, format=None):
        try:
            # Find the product using ID
            product = Product.objects.get(pk=product_id)
            # Get the GroupProduct related to the product
            group_product = GroupProduct.objects.get(id=product.groupproduct.id)
            # Serialize the GroupProduct which includes all related products and latest prices
            serializer = GroupProductSerializer(group_product)
            return Response(serializer.data)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
        except GroupProduct.DoesNotExist:
            return Response({'error': 'GroupProduct not found for the given product'}, status=status.HTTP_404_NOT_FOUND)


from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import ShoppingList, ListItem, Product
from .serializers import ShoppingListSerializer, ListItemSerializer


from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import ShoppingList, CustomUser
from .serializers import ShoppingListSerializer

@api_view(['POST'])
def create_shopping_list(request):
    user = request.user
    name = request.data.get('name')
    if not name:
        return Response({'error': 'Name is required'}, status=400)
    shopping_list = ShoppingList.objects.create(user=user, name=name)
    serializer = ShoppingListSerializer(shopping_list)
    return Response(serializer.data, status=201)


@api_view(['GET'])
def get_shopping_lists(request):
    user = request.user
    shopping_lists = ShoppingList.objects.filter(user=user)
    serializer = ShoppingListSerializer(shopping_lists, many=True)
    return Response(serializer.data)


from .models import ListItem, Product

@api_view(['POST'])
def add_product_to_list(request):
    # Extract data from the POST request
    list_id = request.data.get('listId')
    product_id = request.data.get('productId')
    quantity = request.data.get('quantity', 1)  # Default quantity to 1 if not specified

    # Get the list and product instances
    shopping_list = get_object_or_404(ShoppingList, id=list_id)
    product = get_object_or_404(Product, id=product_id)

    # Create a new list item or update existing one
    list_item, created = ListItem.objects.update_or_create(
        shoppinglist=shopping_list,
        product=product,
        defaults={'quantity': quantity}
    )

    return Response({
        "status": "success",
        "message": "Product added to list successfully",
        "listId": list_id,
        "productId": product_id,
        "quantity": quantity
    })

import googlemaps
from django.conf import settings
from django.http import JsonResponse
import geopy.distance

gmaps = googlemaps.Client(key=settings.GOOGLE_MAPS_API_KEY)

def find_supermarkets(request):
    user_location = None
    if 'address' in request.GET:
        geocode_result = gmaps.geocode(request.GET['address'])
        if geocode_result:
            user_location = geocode_result[0]['geometry']['location']
    elif 'latitude' in request.GET and 'longitude' in request.GET:
        user_location = {
            'lat': float(request.GET['latitude']),
            'lng': float(request.GET['longitude'])
        }

    if user_location:
        places_result = gmaps.places_nearby(
            location=user_location,
            keyword="supermarket",
            type="supermarket",
            rank_by="distance"
        )
        
        supermarkets = []
        for place in places_result['results']:
            details = gmaps.place(place_id=place['place_id'])['result']
            supermarket_info = {
                'name': details['name'],
                'address': details.get('formatted_address', ''),
                'opening_times': details.get('opening_hours', {}).get('weekday_text', []),
                'distance': geopy.distance.distance(
                    (user_location['lat'], user_location['lng']),
                    (details['geometry']['location']['lat'], details['geometry']['location']['lng'])
                ).km
            }
            supermarkets.append(supermarket_info)

        return JsonResponse({'supermarkets': supermarkets})
    else:
        return JsonResponse({'error': 'No valid location provided'}, status=400)



import matplotlib.pyplot as plt
from django.http import HttpResponse
from matplotlib.dates import DateFormatter, AutoDateLocator
import io
from rest_framework.views import APIView
from .models import Product, ProductPrice
import matplotlib.dates as mdates

class ProductPriceHistoryChartView(APIView):
    """
    Generate a chart for price history of all products in a specific group across different supermarkets.
    This endpoint returns an image of the chart.
    """

    def get(self, request, groupproduct_id):
        # Color mapping for different supermarkets
        colors = {
            'Tesco': 'navy',
            'Sainsbury\'s': 'orange',
            'Asda': 'lime',
            'Morrisons': 'darkgreen'
        }

        # Create a new figure with a single subplot
        fig, ax = plt.subplots()

        # Query the database for products linked to the specified group ID
        products = Product.objects.filter(groupproduct_id=groupproduct_id).select_related('supermarket')
        
        if not products:
            return HttpResponse("No products found for the provided group ID.", status=404)

        for product in products:
            # Get price history sorted by date
            prices = ProductPrice.objects.filter(product=product).order_by('datetime_price_updated')
            if not prices:
                continue

            # Extract dates and the minimum available price for each entry
            dates = [price.datetime_price_updated for price in prices]
            min_prices = [min(price.rrp_price, price.sale_price or price.rrp_price, price.loyalty_card_price or price.rrp_price) for price in prices]

            # Plot the data
            ax.plot_date(dates, min_prices, '-', label=f"{product.product_name} ({product.supermarket.supermarket_name})", 
                         color=colors.get(product.supermarket.supermarket_name, 'gray'))

        # Formatting the plot with date ticks, labels, and a legend
        ax.xaxis.set_major_locator(AutoDateLocator())
        ax.xaxis.set_major_formatter(DateFormatter('%Y-%m'))
        ax.set_xlabel('Date')
        ax.set_ylabel('Price (£)')
        ax.set_title('Price History Chart')
        ax.legend()
        plt.xticks(rotation=45)
        plt.tight_layout()

        # Save the plot to a bytes buffer
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        plt.close(fig)
        buffer.seek(0)

        # Return the plot as a PNG image response
        return HttpResponse(buffer.getvalue(), content_type='image/png')

