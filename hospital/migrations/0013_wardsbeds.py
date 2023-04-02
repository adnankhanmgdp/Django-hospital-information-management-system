# Generated by Django 3.2.16 on 2023-02-14 18:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0012_patient_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='WardsBeds',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ward', models.CharField(max_length=255)),
                ('floor', models.CharField(max_length=255)),
                ('beds', models.CharField(max_length=10)),
                ('addedby', models.CharField(max_length=255)),
            ],
        ),
    ]