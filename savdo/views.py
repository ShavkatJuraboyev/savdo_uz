from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils.translation import activate
from savdo.models import Category, Product, Order, Gallery
from savdo.translations import TRANSLATIONS
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt


def set_language(request):
    language = request.GET.get('lang', 'en')
    activate(language)
    request.session['django_language'] = language
    response = redirect(request.META.get("HTTP_REFERER", '/'))
    response.set_cookie('django_language', language)
    return response

@csrf_exempt
def index(request):
    if request.method == "POST":
        full_name = request.POST.get("full_name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        note = request.POST.get("note")
        if all([full_name, email, phone]):
            Order.objects.create(
                full_name=full_name,
                email=email,
                phone=phone,
                note=note
            )
            messages.success(request, "Xabaringiz muvaffaqiyatli qabul qilindi!")
            return redirect("index")
        else:
            messages.error(request, "Iltimos, barcha majburiy maydonlarni to‘ldiring.")
    
    gallery = Gallery.objects.all()[:9]  # So‘nggi 10 ta rasmni olish
    language = request.session.get('django_language', 'en')
    categories = Category.objects.all()
    products_by_category = {}

    all_products = Product.objects.filter(available=True)
    for product in all_products:
        product.name_trans = product.get_name(language)
        product.description_trans = product.get_description(language)
        product.ingredients_trans = product.get_ingredients(language)

    all_paginator = Paginator(all_products, 12)
    all_page_number = request.GET.get("page_all", 1)
    all_paginated_products = all_paginator.get_page(all_page_number)

    # Kategoriya bo‘yicha mahsulotlar
    for category in categories:
        category_products = Product.objects.filter(category=category, available=True)

        for product in category_products:
            product.name_trans = product.get_name(language)
            product.description_trans = product.get_description(language)
            product.ingredients_trans = product.get_ingredients(language)

        paginator = Paginator(category_products, 12)
        page_number = request.GET.get(f'page_{category.slug}', 1)
        paginated_products = paginator.get_page(page_number)

        products_by_category[category.slug] = paginated_products

    menu_text = TRANSLATIONS['menu'].get(language, TRANSLATIONS['menu']['en'])

    context = {
        'categories': categories,
        'products_by_category': products_by_category,
        'all_products': all_paginated_products,
        'menu_text': menu_text,
        'language': language,
        'gallery': gallery,
        'active_page': 'index',
    }
    return render(request, 'base/index.html', context)


def shop_detail(request, slug):
    language = request.session.get('django_language', 'en')
    product = get_object_or_404(Product, slug=slug)
    related_products = Product.objects.filter(category=product.category).exclude(slug=product.slug)
    menu_text = TRANSLATIONS['menu'].get(language, TRANSLATIONS['menu']['en'])
    for related_product in related_products:
            related_product.name_trans = related_product.get_name(language)
            related_product.description_trans = related_product.get_description(language)
            related_product.ingredients_trans = related_product.get_ingredients(language)
    
    product.name_trans = product.get_name(language)
    product.description_trans = product.get_description(language)
    product.ingredients_trans = product.get_ingredients(language)
    ctx ={
        'product': product, 
        'related_products': related_products, 
        'language': language, 
        'menu_text': menu_text}
    return render(request, 'base/shop-detail.html', ctx)

def about(request):
    return render(request, 'base/about.html')


def make_order(request):
    if request.method == "POST":
        # Foydalanuvchi ma'lumotlarini olish
        full_name = request.POST.get("full_name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        note = request.POST.get("note")
        # Majburiy maydonlar to‘ldirilganligini tekshirish
        if all([full_name, email, phone]):
            # Buyurtmani yaratish
            order = Order.objects.create(
                full_name=full_name,
                email=email,
                phone=phone,
                note=note
            )

            messages.success(request, "Xabaringiz muvaffaqiyatli qabul qilindi!")
            return redirect("index")  # O'zgartiring: 'home' o‘rniga kerakli sahifa nomini yozing
        else:
            messages.error(request, "Iltimos, barcha majburiy maydonlarni to‘ldiring.")
    return render(request, "base/chackout.html")
