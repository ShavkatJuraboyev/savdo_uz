from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils.translation import activate, get_language
from django.core.paginator import Paginator
from django.core.mail import send_mail

from savdo.models import Category, Product, Order, Gallery, Certificate, News
from savdo.translations import TRANSLATIONS


def set_language(request):
    language = request.GET.get("lang", "en")
    activate(language)
    response = redirect(request.META.get("HTTP_REFERER", "/"))
    response.set_cookie("django_language", language)
    return response


def index(request):
    # =========================
    # CONTACT FORM
    # =========================
    if request.method == "POST":
        full_name = request.POST.get("full_name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        note = request.POST.get("note")

        if full_name and email and phone:
            Order.objects.create(
                full_name=full_name,
                email=email,
                phone=phone,
                note=note,
            )

            # Email yuborish
            subject = "Yangi murojaat"
            html_message = f"""
                <h2>Yangi murojaat</h2>
                <p><b>Ism:</b> {full_name}</p>
                <p><b>Email:</b> {email}</p>
                <p><b>Telefon:</b> {phone}</p>
                <p><b>Xabar:</b> {note}</p>
            """

            send_mail(
                subject,
                "",
                "no-reply@yourdomain.com",  # from_email
                ["devpysh@gmail.com"],
                html_message=html_message,
            )

            messages.success(request, "Xabaringiz muvaffaqiyatli yuborildi!")
            return redirect("index")

        else:
            messages.error(request, "Iltimos barcha majburiy maydonlarni to‘ldiring.")

    # =========================
    # PRODUCTS
    # =========================
    language = get_language()
    categories = Category.objects.all()
    gallery = Gallery.objects.all()[:9]
    certificates = Certificate.objects.all()[:9]

    products = Product.objects.filter(available=True)

    # tarjimalar
    for product in products:
        product.name_trans = product.get_name(language)
        product.description_trans = product.get_description(language)
        product.content_trans = product.get_content(language)

    paginator = Paginator(products, 12)
    page = request.GET.get("page_all")
    all_products = paginator.get_page(page)

    # kategoriya bo‘yicha
    products_by_category = {}
    for category in categories:
        cat_products = products.filter(category=category)

        paginator = Paginator(cat_products, 12)
        page = request.GET.get(f"page_{category.slug}")
        products_by_category[category.slug] = paginator.get_page(page)

    menu_text = TRANSLATIONS["menu"].get(language, TRANSLATIONS["menu"]["en"])

    # Yangiliklar (6 ta)
    news_list = News.objects.order_by("-created_at")[:6]

    for n in news_list:
        n.title_trans = n.get_title(language)
        n.text_trans = n.get_text(language)
        n.img_url = n.get_img()  # url yoki None


    context = {
        "categories": categories,
        "products_by_category": products_by_category,
        "all_products": all_products,
        "menu_text": menu_text,
        "language": language,
        "gallery": gallery,
        "certificates": certificates,
        "news_list": news_list,
    }

    return render(request, "base/index.html", context)


def shop_detail(request, slug):
    language = get_language()
    product = get_object_or_404(Product, slug=slug)

    product.name_trans = product.get_name(language)
    product.description_trans = product.get_description(language)
    product.content_trans = product.get_content(language)

    menu_text = TRANSLATIONS["menu"].get(language, TRANSLATIONS["menu"]["en"])

    return render(
        request,
        "base/shop-detail.html",
        {
            "product": product,
            "language": language,
            "menu_text": menu_text,
        },
    )


def about(request):
    return render(request, "base/about.html")


def news(request):
    language = get_language()
    menu_text = TRANSLATIONS["menu"].get(language, TRANSLATIONS["menu"]["en"])
    news = News.objects.order_by("-created_at")

    for n in news:
        n.title_trans = n.get_title(language)
        n.text_trans = n.get_text(language)
        n.img_url = n.get_img()

    paginator = Paginator(news, 3)
    page = request.GET.get("page")
    all_news = paginator.get_page(page)

    context = {
        "menu_text": menu_text,
        "all_news": all_news,
        "language": language,
    }
    return render(request, "base/news.html", context)

def news_detail(request, id):
    language = get_language()
    menu_text = TRANSLATIONS["menu"].get(language, TRANSLATIONS["menu"]["en"])

    news = get_object_or_404(News, id=id)

    # title/text
    news.title_trans = news.get_title(language)
    news.text_trans = news.get_text(language)

    # rasm
    news.img_url = news.get_img()

    # CKEditor content (asosiy matn)
    # uz/ru/en dan qaysi biri bo'lsa shuni oladi, bo'sh bo'lsa en ga fallback
    news.content_trans = getattr(news, f"content_{language}", None) or news.content_en or ""

    return render(
        request,
        "base/news_detail.html",
        {
            "news": news,
            "menu_text": menu_text,
            "language": language,
        },
    )
