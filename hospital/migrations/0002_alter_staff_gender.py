# Generated by Django 3.2.16 on 2023-01-15 17:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staff',
            name='gender',
            field=models.CharField(max_length=6),
        ),
    ]
