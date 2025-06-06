# Generated by Django 5.2.1 on 2025-05-29 09:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('savdo', '0005_product_all_files'),
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title_uz', models.CharField(max_length=200, verbose_name='Yangilik sarlavhasi (UZ)')),
                ('title_ru', models.CharField(blank=True, max_length=200, null=True, verbose_name='Yangilik sarlavhasi (RU)')),
                ('title_en', models.CharField(blank=True, max_length=200, null=True, verbose_name='Yangilik sarlavhasi (EN)')),
                ('text_uz', models.TextField(blank=True, null=True, verbose_name='Yangilik matni (UZ)')),
                ('text_ru', models.TextField(blank=True, null=True, verbose_name='Yangilik matni (RU)')),
                ('text_en', models.TextField(blank=True, null=True, verbose_name='Yangilik matni (EN)')),
                ('image', models.ImageField(blank=True, null=True, upload_to='news/', verbose_name='Yangilik rasmi')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Yaratilgan vaqti')),
            ],
            options={
                'verbose_name': 'Yangilik',
                'verbose_name_plural': 'Yangiliklar',
            },
        ),
    ]
