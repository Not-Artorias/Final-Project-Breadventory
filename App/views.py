from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError,transaction
from .models import Product, Ingredient, Sale, SaleItem
from django.utils.timezone import now
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView
from .models import Ingredient
from decimal import Decimal


# Ingredients Login Register table

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                login(request, user)
                return redirect('index')
            except IntegrityError:
                form.add_error('username', 'This username is already taken. Please choose another one.')
        else:
            form.add_error(None, 'There was an error with your form. Please check the fields.')
    else:
        form = UserCreationForm()

    return render(request, 'App/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
        else:
            return render(request, 'App/login.html', {'form': form})
    else:
        form = AuthenticationForm()
    return render(request, 'App/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

 #Ingredients table
@login_required
def index(request):
    products = Product.objects.all()
    return render(request, 'App/index.html', {'products': products})

@login_required
def ingredients(request):
    ingredients = Ingredient.objects.all()
    return render(request, 'App/ingredients.html', {'ingredients': ingredients})

 #Sale table
@login_required
def Saletable(request):
    sales = Sale.objects.all().order_by('-sale_time')
    return render(request, 'App/saletable.html', {'sales': sales})


@login_required
def saleadd(request):
    products = Product.objects.all()

    if request.method == 'POST':
        valid_sale = False
        with transaction.atomic():
            sale = Sale.objects.create(user=request.user)

            for product in products:
                qty_str = request.POST.get(f'qty_{product.id}')
                if qty_str:
                    try:
                        qty = int(qty_str)
                        if qty > 0 and qty <= product.stock_qty:
                            valid_sale = True
                            subtotal = qty * product.price
                            SaleItem.objects.create(
                                sale=sale,
                                product=product,
                                quantity=qty,
                                subtotal=subtotal
                            )
                            product.stock_qty -= qty
                            product.save()
                    except ValueError:
                        pass

        if valid_sale:
            return redirect('Saletable')
        else:
            return render(request, 'App/saleadd.html', {'products': products, 'error': 'Please enter a quantity greater than 0 for at least one product.'})

    return render(request, 'App/saleadd.html', {'products': products})
@login_required
def void_sale(request, sale_id):
    sale = get_object_or_404(Sale, id=sale_id)
    if request.method == 'POST':
        sale.is_voided = True
        sale.save()
    return redirect('Saletable')

 #Salesitem table

@login_required
def saleitem(request, sale_id):
    sale = get_object_or_404(Sale, id=sale_id)
    sale_items = SaleItem.objects.filter(sale=sale)
    return render(request, 'App/saleitem.html', {'sale': sale, 'sale_items': sale_items})


def saleadditem(request, sale_id):
    sale = get_object_or_404(Sale, id=sale_id)
    products = Product.objects.all()
    sale_items = SaleItem.objects.filter(sale=sale)

    if request.method == 'POST':
        product_id = request.POST.get('product')
        quantity = int(request.POST.get('quantity'))

        product = get_object_or_404(Product, id=product_id)
        subtotal = product.price * quantity

        SaleItem.objects.create(
            sale=sale,
            product=product,
            quantity=quantity,
            subtotal=subtotal,
            is_voided=False
        )

        return redirect('saleadditem', sale_id=sale.id)

    return render(request, 'App/saleadditem.html', {
        'sale': sale,
        'products': products,
        'sale_items': sale_items
    })


def void_sale_item(request, item_id):
    item = get_object_or_404(SaleItem, id=item_id)

    item.is_voided = True
    item.save()

    return redirect('saleitem', sale_id=item.sale.id)
 #Product table

@login_required
def product_list(request):
    products = Product.objects.all()
    return render(request, 'App/product_list.html', {'products': products})

@login_required
def product_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        stock_qty = request.POST.get('stock_qty')
        image = request.FILES.get('image')

        if not stock_qty:
            stock_qty = 0
        else:
            try:
                stock_qty = int(stock_qty)
            except ValueError:
                stock_qty = 0

        Product.objects.create(
            name=name,
            description=description,
            price=price,
            stock_qty=stock_qty,
            image=image
        )
        return redirect('product_list')
    return render(request, 'App/product_create.html')

@login_required
def product_update(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        stock_qty = request.POST.get('stock_qty')
        
        if request.FILES.get('image'):
            product.image = request.FILES.get('image')
            
        product.name = name
        product.description = description
        product.price = price
        product.stock_qty = stock_qty
        product.save()

        return redirect('product_list')

    return render(request, 'App/product_update.html', {'product': product})


@login_required
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('product_list')
    return render(request, 'App/product_delete.html', {'product': product})

 #Ingredient again table

@login_required
def ingredient_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        unit = request.POST.get('unit')
        stock_qty = request.POST.get('stock_qty')
        expiration_date = request.POST.get('expiration_date')

        Ingredient.objects.create(
            name=name,
            unit=unit,
            stock_qty=stock_qty,
            expiration_date=expiration_date
        )
        return redirect('ingredients')

    return render(request, 'App/ingredient_create.html')

@login_required
def ingredient_update(request, ingredient_id):
    ingredient = get_object_or_404(Ingredient, id=ingredient_id)

    if request.method == 'POST':
        ingredient.name = request.POST.get('name')
        ingredient.unit = request.POST.get('unit')
        ingredient.stock_qty = request.POST.get('stock_qty')
        ingredient.expiration_date = request.POST.get('expiration_date')
        ingredient.save()
        return redirect('ingredients')

    return render(request, 'App/ingredient_update.html', {'ingredient': ingredient})

@login_required
def ingredient_delete(request, ingredient_id):
    ingredient = get_object_or_404(Ingredient, id=ingredient_id)

    if request.method == 'POST':
        ingredient.delete()
        return redirect('ingredients')

    return render(request, 'App/ingredient_delete.html', {'ingredient': ingredient})