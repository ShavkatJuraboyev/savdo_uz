from django.db import models

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Maxsalat turi')
    slug = models.SlugField(max_length=100, unique=True, verbose_name='Maxsalat turi slug')
    description = models.TextField(verbose_name='Maxsalat turi haqida')
    image = models.ImageField(upload_to='categories/', verbose_name='Maxsalat turi rasmi', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Yaratilgan vaqti')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='O\'zgartirilgan vaqti')

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'Maxsalat turlari'
        verbose_name = 'Maxsalat turi'
    

class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name='Maxsalat nomi')
    slug = models.SlugField(max_length=100, unique=True, verbose_name='Maxsalat nomi slug')
    description = models.TextField(verbose_name='Maxsalat haqida')
    ingredients = models.TextField(verbose_name='Maxsalat tarkibi')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Maxsalat narxi')
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='Maxsalat chegirmali narxi')
    stock = models.IntegerField(verbose_name='Maxsalat miqdori')
    available = models.BooleanField(default=True, verbose_name='Maxsalat mavjudligi')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Maxsalat turi')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Yaratilgan vaqti')
    image = models.ImageField(upload_to='products/', verbose_name='Maxsalat rasmi')

    def get_image_url(self):
        if self.image:
            return self.image.url
        return None

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'Maxsalatlar'
        verbose_name = 'Maxsalat'


class Order(models.Model):
    full_name = models.CharField(max_length=100, verbose_name="To‘liq ismi")
    email = models.EmailField(verbose_name="Email manzil")
    phone = models.CharField(max_length=20, verbose_name="Telefon raqam")
    city = models.CharField(max_length=100, verbose_name="Shahar")
    district = models.CharField(max_length=100, verbose_name="Tuman")
    street = models.CharField(max_length=100, verbose_name="Ko‘cha")
    house_number = models.CharField(max_length=100, verbose_name="Uy raqami")
    apartment_number = models.CharField(max_length=100, verbose_name="Xonadon raqami", blank=True, null=True)
    address = models.TextField(verbose_name="Manzil")
    note = models.TextField(verbose_name="Izoh", blank=True, null=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Jami narx")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Buyurtma vaqti")

    def __str__(self):
        return f"{self.full_name} - {self.phone}"
    
    class Meta:
        verbose_name = "Buyurtma"
        verbose_name_plural = "Buyurtmalar"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name="Buyurtma")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Maxsulot")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Soni")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Narxi")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan vaqti")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="O'zgartirilgan vaqti")

    def __str__(self):
        return f"{self.product.name} ({self.quantity})"
    
    class Meta:
        verbose_name = "Buyurtma mahsuloti"
        verbose_name_plural = "Buyurtma mahsulotlari"
