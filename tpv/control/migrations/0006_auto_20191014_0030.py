# Generated by Django 2.2.6 on 2019-10-14 06:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control', '0005_auto_20191014_0022'),
    ]

    operations = [
        migrations.AddField(
            model_name='detallepedido',
            name='cantidad',
            field=models.DecimalField(decimal_places=0, default=1, max_digits=10),
        ),
        migrations.AddField(
            model_name='detallepedido',
            name='precio',
            field=models.DecimalField(decimal_places=0, default=1, max_digits=10),
        ),
    ]