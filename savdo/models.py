from django.db import models
from django.utils.translation import gettext_lazy as _
from ckeditor_uploader.fields import RichTextUploadingField 

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

    content_uz = RichTextUploadingField(config_name='extends_uz', verbose_name="Sarlovha umumiy matini", null=True, blank=True)
    content_en = RichTextUploadingField(config_name='extends_en', verbose_name="English sarlovha umumiy matini", null=True, blank=True)
    content_ru = RichTextUploadingField(config_name='extends_ru', verbose_name="Ruscha sarlovha umumiy matini", null=True, blank=True)

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

    def get_content(self, language):
        return self.get_translation('content', language)

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

class Certificate(models.Model):
    image = models.ImageField(upload_to='certificates/', verbose_name=_('Sertifikat rasmi'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Yaratilgan vaqti'))

    def __str__(self):
        return f"Certificate {self.id}"

    def get_image_url(self):
        if self.image:
            return self.image.url
        return None
    
    class Meta:
        verbose_name = _('Sertifikat')
        verbose_name_plural = _('Sertifikatlar')


class News(models.Model):
    title_uz = models.CharField(max_length=200, verbose_name=_('Yangilik sarlavhasi (UZ)'))
    title_ru = models.CharField(max_length=200, verbose_name=_('Yangilik sarlavhasi (RU)'), blank=True, null=True)
    title_en = models.CharField(max_length=200, verbose_name=_('Yangilik sarlavhasi (EN)'), blank=True, null=True)

    text_uz = models.TextField(verbose_name=_('Yangilik matni (UZ)'), null=True, blank=True)
    text_ru = models.TextField(verbose_name=_('Yangilik matni (RU)'), null=True, blank=True)        
    text_en = models.TextField(verbose_name=_('Yangilik matni (EN)'), null=True, blank=True)

    # content_uz = RichTextUploadingField(config_name='extends_uz', verbose_name="Yangilik matni (UZ)", null=True, blank=True)
    # content_en = RichTextUploadingField(config_name='extends_en', verbose_name="Yangilik matni (EN)", null=True, blank=True)
    # content_ru = RichTextUploadingField(config_name='extends_ru', verbose_name="Yangilik matni (RU)", null=True, blank=True)

    image = models.ImageField(upload_to='news/', verbose_name=_('Yangilik rasmi'), null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Yaratilgan vaqti'))

    def __str__(self):
        return self.title_uz

    class Meta:
        verbose_name_plural = _('Yangiliklar')
        verbose_name = _('Yangilik')

    def get_translation(self, field_name, language):
        """Berilgan tilga mos tarjimani qaytaradi."""
        language_suffix = f"_{language}"
        translated_field = f"{field_name}{language_suffix}"
        return getattr(self, translated_field, getattr(self, f"{field_name}_en", ''))

    def get_title(self, language):
        return self.get_translation('title', language)

    def get_text(self, language):
        return self.get_translation('text', language)
    
    def get_img(self):
        if self.image:
            return self.image.url
        return None