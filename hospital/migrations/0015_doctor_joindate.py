# Generated by Django 3.2.16 on 2023-02-16 17:22

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0014_doctor'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctor',
            name='joindate',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
