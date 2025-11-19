from django.shortcuts import render
from . import models

# Create your views here.
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
