# Generated by Django 4.2.5 on 2023-09-13 00:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myshop', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='productimage',
            name='product_image',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
    ]
