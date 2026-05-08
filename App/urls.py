from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings # NEW
from django.conf.urls.static import static # NEW

urlpatterns = [
    path('', views.index, name='index'),

    # Login URLs
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    # Using the built-in LogoutView is cleaner
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

    # Ingredients URLs
    path('ingredients/', views.ingredients, name='ingredients'),
    path('ingredients/create/', views.ingredient_create, name='ingredient_create'),
    path('ingredients/update/<int:ingredient_id>/', views.ingredient_update, name='ingredient_update'),
    path('ingredients/delete/<int:ingredient_id>/', views.ingredient_delete, name='ingredient_delete'),

    # Sales URLs
    path('sales/', views.Saletable, name='Saletable'),
    path('sales/add/', views.saleadd, name='saleadd'),
    path('sale/void/<int:sale_id>/', views.void_sale, name='void_sale'),

    # Sale Item URLs
    path('sale/items/<int:sale_id>/', views.saleitem, name='saleitem'),
    path('sales/add/<int:sale_id>/', views.saleadditem, name='saleadditem'),
    path('saleitem/void/<int:item_id>/', views.void_sale_item, name='void_sale_item'),

    # Products URLs
    path('products/', views.product_list, name='product_list'),
    path('products/create/', views.product_create, name='product_create'),
    path('products/update/<int:product_id>/', views.product_update, name='product_update'),
    path('products/delete/<int:pk>/', views.product_delete, name='product_delete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)