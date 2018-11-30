# Generated by Django 2.0.5 on 2018-05-12 11:53

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('supermercadoApp', '0012_auto_20180512_1029'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usuario_supermercado',
            name='supermercado',
        ),
        migrations.RemoveField(
            model_name='usuario_supermercado',
            name='usuario',
        ),
        migrations.AlterField(
            model_name='carrito',
            name='fecha_inicio',
            field=models.DateTimeField(default=datetime.datetime(2018, 5, 12, 11, 53, 47, 636512)),
        ),
        migrations.AlterField(
            model_name='factura',
            name='fecha',
            field=models.DateTimeField(default=datetime.datetime(2018, 5, 12, 11, 53, 47, 637395)),
        ),
        migrations.AlterField(
            model_name='mensaje_cliente',
            name='cliente',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='supermercadoApp.Cliente'),
        ),
        migrations.AlterField(
            model_name='mensaje_cliente',
            name='fecha',
            field=models.DateTimeField(default=datetime.datetime(2018, 5, 12, 11, 53, 47, 634222)),
        ),
        migrations.AlterField(
            model_name='tarjeta',
            name='cliente',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='supermercadoApp.Cliente'),
        ),
        migrations.AlterField(
            model_name='tarjeta',
            name='fecha_adquisicion',
            field=models.DateTimeField(default=datetime.datetime(2018, 5, 12, 11, 53, 47, 635547)),
        ),
        migrations.DeleteModel(
            name='Usuario_Supermercado',
        ),
    ]