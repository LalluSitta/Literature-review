# Generated by Django 5.1.5 on 2025-03-11 13:45

import shortuuid.main
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articoli', '0017_alter_articoli_id_alter_articoli_lingua'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articoli',
            name='id',
            field=models.CharField(default=shortuuid.main.ShortUUID.uuid, editable=False, max_length=22, primary_key=True, serialize=False),
        ),
    ]
