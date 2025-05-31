from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils.translation import activate
from savdo.models import Category, Product, Order, Gallery, Certificate, News
from savdo.translations import TRANSLATIONS
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail


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

        subject = "Yangi Murojaat"
        message = f"""
            <html>
                <body style="margin: 0; padding: 0; font-family: Arial, sans-serif; background-color: #f4f4f4;">
                    <div style="max-width: 600px; margin: 30px auto; background-color: #ffffff; border-radius: 10px; overflow: hidden; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);">
                    
                    <div style="background: linear-gradient(135deg, #3498db, #8e44ad); color: white; padding: 20px 30px; text-align: center;">
                        <h2 style="margin: 0;">📩 Yangi murojaat tafsilotlari</h2>
                    </div>

                    <div style="padding: 30px;">
                        <table style="width: 100%; border-collapse: collapse;">
                        <tr>
                            <td style="padding: 12px 0; font-weight: bold; color: #555;">👤 Ism:</td>
                            <td style="padding: 12px 0; color: #333;">{full_name}</td>
                        </tr>
                        <tr>
                            <td style="padding: 12px 0; font-weight: bold; color: #555;">📧 Email:</td>
                            <td style="padding: 12px 0; color: #333;">{email}</td>
                        </tr>
                        <tr>
                            <td style="padding: 12px 0; font-weight: bold; color: #555;">📱 Telefon:</td>
                            <td style="padding: 12px 0; color: #333;">{phone}</td>
                        </tr>
                        <tr>
                            <td style="padding: 12px 0; font-weight: bold; color: #555;">📝 Xabar:</td>
                            <td style="padding: 12px 0; color: #333;">{note}</td>
                        </tr>
                        </table>
                    </div>

                    <div style="background-color: #f0f0f0; padding: 15px 30px; text-align: center; color: #888; font-size: 13px;">
                        Ushbu xabar sizning sayt orqali yuborildi.
                    </div>
                    </div>
                </body>
            </html>
        """
        admin_email = 'devpysh@gmail.com'
        send_mail(subject, '', email, [admin_email], html_message=message)

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
    # Sertifikatlar
    certificates = Certificate.objects.all()[:9]  # So‘nggi 10 ta sertifikatni olish
    # Sertifikatlar
    language = request.session.get('django_language', 'en')
    categories = Category.objects.all()
    products_by_category = {}

    all_products = Product.objects.filter(available=True)
    for product in all_products:
        product.name_trans = product.get_name(language)
        product.description_trans = product.get_description(language)
        product.content_trans = product.get_content(language)

    all_paginator = Paginator(all_products, 12)
    all_page_number = request.GET.get("page_all", 1)
    all_paginated_products = all_paginator.get_page(all_page_number)

    # Kategoriya bo‘yicha mahsulotlar
    for category in categories:
        category_products = Product.objects.filter(category=category, available=True)

        for product in category_products:
            product.name_trans = product.get_name(language)
            product.description_trans = product.get_description(language)
            product.content_trans = product.get_content(language)

        paginator = Paginator(category_products, 12)
        page_number = request.GET.get(f'page_{category.slug}', 1)
        paginated_products = paginator.get_page(page_number)

        products_by_category[category.slug] = paginated_products

    menu_text = TRANSLATIONS['menu'].get(language, TRANSLATIONS['menu']['en'])
    news = News.objects.first()
    if news:
        news.title = getattr(news, f'title_{language}', news.title_en)
        news.text = getattr(news, f'text_{language}', news.text_en)

    context = {
        'categories': categories,
        'products_by_category': products_by_category,
        'all_products': all_paginated_products,
        'menu_text': menu_text,
        'language': language,
        'gallery': gallery,
        'active_page': 'index',
        'certificates': certificates,
        'news': news,
    }
    return render(request, 'base/index.html', context)


def shop_detail(request, slug):
    language = request.session.get('django_language', 'en')
    product = get_object_or_404(Product, slug=slug)
    menu_text = TRANSLATIONS['menu'].get(language, TRANSLATIONS['menu']['en'])
    
    product.name_trans = product.get_name(language)
    product.description_trans = product.get_description(language)
    product.content_trans = product.get_content(language)
    ctx ={
        'product': product, 
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
