# Generated by Django 4.2.3 on 2023-07-22 10:53

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0006_remove_order_item_remove_order_quantity_orderitem'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='restaurant.item'),
            preserve_default=False,
        ),
    ]