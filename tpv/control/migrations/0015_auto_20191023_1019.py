# Generated by Django 2.2.6 on 2019-10-23 16:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control', '0014_auto_20191020_1527'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pedido',
            name='observacion',
            field=models.CharField(default='Ninguna', max_length=200),
        ),
        migrations.AlterField(
            model_name='venta',
            name='total',
            field=models.CharField(default=0, max_length=200),
        ),
    ]
