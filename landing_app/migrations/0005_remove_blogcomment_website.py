# Generated by Django 4.1.5 on 2023-02-03 23:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("landing_app", "0004_productcategory_productimage_supplier_stock_product"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="blogcomment",
            name="website",
        ),
    ]
