# Generated by Django 2.2 on 2022-01-25 20:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('personal_project_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='is_vendor',
            field=models.CharField(max_length=50),
        ),
    ]