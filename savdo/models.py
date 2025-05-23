from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.


class Category(models.Model):
    name_uz = models.CharField(max_length=100, verbose_name=_('Maxsalat turi (UZ)'))
    name_ru = models.CharField(max_length=100, verbose_name=_('Maxsalat turi (RU)'), blank=True, null=True)
    name_en = models.CharField(max_length=100, verbose_name=_('Maxsalat turi (EN)'), blank=True, null=True)
    slug = models.SlugField(max_length=100, unique=True, verbose_name=_('Maxsalat turi slug'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Yaratilgan vaqti'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('O\'zgartirilgan vaqti'))

    def __str__(self):
        return self.name_uz

    class Meta:
        verbose_name_plural = _('Maxsalat turlari')
        verbose_name = _('Maxsalat turi')

    def get_translation(self, field_name, language):
        """Berilgan tilga mos tarjimani qaytaradi."""
        language_suffix = f"_{language}"
        translated_field = f"{field_name}{language_suffix}"
        return getattr(self, translated_field, getattr(self, f"{field_name}_en", ''))

    def get_name(self, language):
        return self.get_translation('name', language)
    
    @property
    def translated_name(self):
        from django.utils.translation import get_language
        language = get_language()  # Joriy tilni aniqlash
        return self.get_name(language)


class Product(models.Model):
    name_uz = models.CharField(max_length=100, verbose_name=_('Maxsalat nomi (UZ)'))
    name_ru = models.CharField(max_length=100, verbose_name=_('Maxsalat nomi (RU)'), blank=True, null=True)
    name_en = models.CharField(max_length=100, verbose_name=_('Maxsalat nomi (EN)'), blank=True, null=True)
    slug = models.SlugField(max_length=100, unique=True, verbose_name=_('Maxsalat nomi slug'))
    description_uz = models.TextField(verbose_name=_('Maxsalat haqida (UZ)'), null=True, blank=True)
    description_ru = models.TextField(verbose_name=_('Maxsalat haqida (RU)'), null=True, blank=True)
    description_en = models.TextField(verbose_name=_('Maxsalat haqida (EN)'), null=True, blank=True)
    ingredients_uz = models.TextField(verbose_name=_('Maxsalat tarkibi (UZ)'), null=True, blank=True)
    ingredients_ru = models.TextField(verbose_name=_('Maxsalat tarkibi (RU)'), null=True, blank=True)
    ingredients_en = models.TextField(verbose_name=_('Maxsalat tarkibi (EN)'), null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('Maxsalat narxi'), null=True, blank=True)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name=_('Maxsalat chegirmali narxi'))
    stock = models.IntegerField(verbose_name=_('Maxsalat miqdori'), null=True, blank=True)
    available = models.BooleanField(default=True, verbose_name=_('Maxsalat mavjudligi'))
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name=_('Maxsalat turi'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Yaratilgan vaqti'))
    image = models.ImageField(upload_to='products/', verbose_name=_('Maxsalat rasmi'))
    files = models.FileField(upload_to='products/files/', verbose_name=_('Maxsalat fayli'), null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('O\'zgartirilgan vaqti'))

    def get_image_url(self):
        if self.image:
            return self.image.url
        return None

    def __str__(self):
        return self.name_uz

    class Meta:
        verbose_name_plural = _('Maxsalatlar')
        verbose_name = _('Maxsalat')

    def get_translation(self, field_name, language):
        """Berilgan tilga mos tarjimani qaytaradi."""
        language_suffix = f"_{language}"
        translated_field = f"{field_name}{language_suffix}"
        return getattr(self, translated_field, getattr(self, f"{field_name}_en", ''))

    def get_name(self, language):
        return self.get_translation('name', language)
    
    def get_description(self, language):
        return self.get_translation('description', language)

    def get_ingredients(self, language):
        return self.get_translation('ingredients', language)

class Order(models.Model):
    full_name = models.CharField(max_length=100, verbose_name=_("To‘liq ismi"))
    email = models.EmailField(verbose_name=_("Email manzil"))
    phone = models.CharField(max_length=20, verbose_name=_("Telefon raqam"))
    note = models.TextField(verbose_name=_("Izoh"), blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Buyurtma vaqti"))

    def __str__(self):
        return f"{self.full_name} - {self.phone}"

    class Meta:
        verbose_name = _("Buyurtma")
        verbose_name_plural = _("Buyurtmalar")


class Gallery(models.Model):
    image = models.ImageField(upload_to='gallery/', verbose_name=_('Rasm'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Yaratilgan vaqti'))

    def __str__(self):
        return f"Gallery Image {self.id}"

    def get_image_url(self):
        if self.image:
            return self.image.url
        return None
    
    class Meta:
        verbose_name = _('Rasm')
        verbose_name_plural = _('Rasmlar')