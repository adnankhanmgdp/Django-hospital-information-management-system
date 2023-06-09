# Generated by Django 3.2.16 on 2023-01-15 17:10

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Roles',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(max_length=255)),
                ('permissions', models.CharField(max_length=11250)),
            ],
        ),
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('fullname', models.CharField(max_length=255)),
                ('email', models.CharField(max_length=255, unique=True)),
                ('password', models.CharField(max_length=255)),
                ('address', models.CharField(max_length=255)),
                ('phone', models.BigIntegerField()),
                ('staffId', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('gender', models.CharField(max_length=1)),
                ('isverifed', models.BooleanField()),
                ('role', models.CharField(max_length=20)),
            ],
        ),
    ]
