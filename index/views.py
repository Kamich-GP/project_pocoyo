from django.shortcuts import render, redirect
from . import models
from . import forms
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django import views

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

# Поиск товара по названию
def search(request):
    if request.method == 'POST':
        # Достаем данные с формы
        search_product = request.POST.get('search_product')
        # Достаем данные из БД
        get_product = models.Product.objects.filter(product_name__iregex=search_product)
        # Передаем данные на фронт
        context = {}
        if get_product:
            context.update(user_pr=search_product, products=get_product)
        else:
            context.update(user_pr=search_product, products='')
        return render(request, 'result.html', context)

# Регистрация (класс представления)
class Register(views.View):
    template_name = 'registration/register.html'

    def get(self, request):
        form = forms.RegForm
        context = {'form': form}
        return render(request, self.template_name, context)

    def post(self, request):
        form = forms.RegForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password2')

            user = User.objects.create_user(username=username,
                                     email=email,
                                     password=password)
            user.save()
            login(request, user)
            return redirect('/')


# Добавление товара в корзину
def add_to_cart(request, pk):
    if request.method == 'POST':
        product = models.Product.objects.get(id=pk)
        user_count = int(request.POST.get('pr_amount'))
        print(user_count)

        if 1 <= user_count <= product.product_count:
            models.Cart.objects.create(user_id=request.user.id,
                                user_product=product,
                                user_pr_amount=user_count).save()
            return redirect('/')
        return redirect(f'/product/{pk}')
