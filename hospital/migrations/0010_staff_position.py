# Generated by Django 3.2.16 on 2023-02-14 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0009_alter_patient_dateofadm'),
    ]

    operations = [
        migrations.AddField(
            model_name='staff',
            name='position',
            field=models.CharField(default='Other', max_length=255),
        ),
    ]
