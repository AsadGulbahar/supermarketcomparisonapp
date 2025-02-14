"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.http import HttpResponse

from django.conf import settings
from django.urls import include, path
from django.conf.urls.static import static

from .views import main_spa
from .views import signup_view, login_view, logout_view
from .views import UserProfileView, SearchResultsView, ProductGroupDetailView, ProductPriceHistoryChartView
from .views import get_shopping_lists, add_product_to_list, create_shopping_list
from .views import find_supermarkets

urlpatterns = [
    path('', main_spa, name='index'),
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('search-results/', SearchResultsView.as_view(), name='search-results'),
    path('product-details/<int:product_id>/', ProductGroupDetailView.as_view(), name='product-group-detail'),
    path('price-history/<int:groupproduct_id>/', ProductPriceHistoryChartView.as_view(), name='product-price-history'),
    path('create-list/', create_shopping_list, name='create-list'),
    path('get-lists/', get_shopping_lists, name='get-lists'),
    path('add-to-list/', add_product_to_list, name='add-to-list'),
    path('find-supermarkets/', find_supermarkets, name='find-supermarkets'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
