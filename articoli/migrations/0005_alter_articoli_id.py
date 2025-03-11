# Generated by Django 5.1.4 on 2025-03-04 09:08

import shortuuid.main
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articoli', '0004_alter_articoli_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articoli',
            name='id',
            field=models.CharField(default=shortuuid.main.ShortUUID.uuid, editable=False, max_length=22, primary_key=True, serialize=False),
        ),
    ]
