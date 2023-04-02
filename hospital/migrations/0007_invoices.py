# Generated by Django 3.2.16 on 2023-01-19 19:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0006_delete_invoices'),
    ]

    operations = [
        migrations.CreateModel(
            name='Invoices',
            fields=[
                ('caseid', models.CharField(max_length=255)),
                ('invoiceid', models.AutoField(primary_key=True, serialize=False)),
                ('path', models.CharField(max_length=300)),
            ],
        ),
    ]