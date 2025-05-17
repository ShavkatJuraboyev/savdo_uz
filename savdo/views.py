from django.shortcuts import render, redirect
from django.contrib import messages
from savdo.models import Category, Product, Order, OrderItem
from decimal import Decimal
from django.core.paginator import Paginator
from django.db.models import Sum
# Create your views here.


def index(request):
    categories = Category.objects.all()
    products_by_category = {}

    for category in categories:
        products_by_category[category.slug] = Product.objects.filter(category=category, available=True)

    best_selling = (
        OrderItem.objects
        .values('product')
        .annotate(total_quantity=Sum('quantity'))
        .order_by('-total_quantity')[:6]  # eng ko‘p sotilgan 8 ta mahsulot
    )

    product_ids = [item['product'] for item in best_selling]
    best_products = Product.objects.filter(id__in=product_ids)

    # ID tartibini saqlab qolish uchun ro‘yxatga tartib beramiz
    best_products = sorted(best_products, key=lambda p: product_ids.index(p.id))



    cxt = {
        'categories': categories,
        'products_by_category': products_by_category,
        'best_products': best_products,
    }
    return render(request, 'index.html', cxt)


def shop_detail(request):
    return render(request, 'shop-detail.html')

def about(request):
    return render(request, 'about.html')


def make_order(request):
    if request.method == "POST":
        # Foydalanuvchi ma'lumotlarini olish
        full_name = request.POST.get("full_name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        city = request.POST.get("city")
        district = request.POST.get("district")
        street = request.POST.get("street")
        house_number = request.POST.get("house_number")
        apartment_number = request.POST.get("apartment_number")
        address = request.POST.get("address")
        note = request.POST.get("note")

        # Mahsulotlar va sonlar
        product_ids = request.POST.getlist("product_ids")     # [1, 2, 3]
        quantities = request.POST.getlist("quantities")       # [1, 2, 1]

        # Majburiy maydonlar to‘ldirilganligini tekshirish
        if all([full_name, email, phone, city, district, street, house_number, address, product_ids]):
            total_price = Decimal('0.00')
            products = []

            # Har bir mahsulotni va uning narxini hisoblash
            for pid, qty in zip(product_ids, quantities):
                try:
                    product = Product.objects.get(id=pid)
                    qty = int(qty)
                    price = product.discount_price if product.discount_price else product.price
                    total_price += price * qty
                    products.append((product, qty, price))
                except Product.DoesNotExist:
                    continue

            # Buyurtmani yaratish
            order = Order.objects.create(
                full_name=full_name,
                email=email,
                phone=phone,
                city=city,
                district=district,
                street=street,
                house_number=house_number,
                apartment_number=apartment_number,
                address=address,
                note=note,
                total_price=total_price
            )

            # Buyurtmaga mahsulotlarni qo‘shish
            for product, qty, price in products:
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=qty,
                    price=price
                )

            messages.success(request, "Buyurtmangiz muvaffaqiyatli qabul qilindi!")
            return redirect("index")  # O'zgartiring: 'home' o‘rniga kerakli sahifa nomini yozing
        else:
            messages.error(request, "Iltimos, barcha majburiy maydonlarni to‘ldiring.")

    # GET so‘rovda mavjud mahsulotlarni ko‘rsatish
    query = request.GET.get('q', '')
    product_list = Product.objects.filter(available=True)
    if query:
        product_list = product_list.filter(name__icontains=query)

    paginator = Paginator(product_list, 8)  # Har bir sahifada 5 ta mahsulot
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'products': page_obj,
        'query': query,
        'page_obj': page_obj
    }
    return render(request, "chackout.html", context)
