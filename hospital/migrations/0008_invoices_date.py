# Generated by Django 3.2.16 on 2023-01-19 19:43

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0007_invoices'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoices',
            name='date',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
