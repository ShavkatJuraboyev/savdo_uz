# Generated by Django 5.2.1 on 2025-05-20 05:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('savdo', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Gallery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='gallery/', verbose_name='Rasm')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Yaratilgan vaqti')),
            ],
            options={
                'verbose_name': 'Rasm',
                'verbose_name_plural': 'Rasmlar',
            },
        ),
    ]
