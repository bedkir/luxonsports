# Generated by Django 3.2 on 2021-06-05 21:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_delete_клиент'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShopCart',
            fields=[
                ('user_id', models.CharField(max_length=45)),
                ('item', models.CharField(blank=True, max_length=45, null=True)),
                ('cart_id', models.AutoField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'shop_cart',
                'managed': False,
            },
        ),
    ]
