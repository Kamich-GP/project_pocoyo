from django.shortcuts import render
from . import models

# Create your views here.
# Главная страница
def home_page(request):
    # Достаем данные из БД
    categories = models.Category.objects.all()
    products = models.Product.objects.all()
    # Передаем данные на Frontend
    context = {
        'categories': categories,
        'products': products
    }
    return render(request, 'home.html', context)

# Страница с товарами по категории
def category_page(request, pk):
    # Достаем данные из БД
    category = models.Category.objects.get(id=pk)
    products = models.Product.objects.filter(product_category=category)
    # Передаем данные на Frontend
    context = {
        'category': category,
        'products': products
    }
    return render(request, 'category.html', context)

# Страница определенного товара
def product_page(request, pk):
    # Достаем данные из БД
    product = models.Product.objects.get(id=pk)
    # Передаем данные на Frontend
    context = {'product': product}
    return render(request, 'product.html', context)
