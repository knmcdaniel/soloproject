# Generated by Django 2.2 on 2022-01-27 05:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('personal_project_app', '0004_products_sale_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='amount_sold',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
