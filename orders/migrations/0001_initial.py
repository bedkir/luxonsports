# Generated by Django 3.2.4 on 2021-06-05 21:02

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AuthUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128)),
                ('last_login', models.DateTimeField(blank=True, null=True)),
                ('is_superuser', models.IntegerField()),
                ('username', models.CharField(max_length=150, unique=True)),
                ('first_name', models.CharField(max_length=150)),
                ('last_name', models.CharField(max_length=150)),
                ('email', models.CharField(max_length=254)),
                ('is_staff', models.IntegerField()),
                ('is_active', models.IntegerField()),
                ('date_joined', models.DateTimeField()),
                ('cart', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'db_table': 'auth_user',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ShopOrder',
            fields=[
                ('id', models.IntegerField(db_column='id', primary_key=True, serialize=False)),
                ('фамилия', models.CharField(max_length=45)),
                ('имя', models.CharField(max_length=45)),
                ('отчество', models.CharField(blank=True, max_length=45, null=True)),
                ('телефон', models.CharField(blank=True, max_length=45, null=True)),
                ('почта', models.CharField(max_length=60)),
                ('заказ', models.CharField(max_length=45)),
                ('сумма_заказа', models.CharField(blank=True, max_length=45, null=True)),
                ('валюта_заказа', models.CharField(blank=True, max_length=45, null=True)),
                ('статус_оплаты', models.CharField(max_length=45)),
                ('статус_заказа', models.CharField(max_length=45)),
                ('адрес_заказа', models.CharField(max_length=90)),
                ('дата_заказа', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'shop_order',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ShopProduct',
            fields=[
                ('id', models.IntegerField(db_column='id', primary_key=True, serialize=False)),
                ('код_товара', models.CharField(blank=True, db_column='Код_товара', max_length=25, null=True)),
                ('название_позиции', models.CharField(db_column='Название_позиции', max_length=98)),
                ('название_позиции_укр', models.CharField(blank=True, db_column='Название_позиции_укр', max_length=90, null=True)),
                ('поисковые_запросы', models.CharField(blank=True, db_column='Поисковые_запросы', max_length=171, null=True)),
                ('поисковые_запросы_укр', models.CharField(blank=True, db_column='Поисковые_запросы_укр', max_length=169, null=True)),
                ('описание', models.CharField(blank=True, db_column='Описание', max_length=5231, null=True)),
                ('описание_укр', models.CharField(blank=True, db_column='Описание_укр', max_length=6656, null=True)),
                ('тип_товара', models.CharField(blank=True, db_column='Тип_товара', max_length=1, null=True)),
                ('цена', models.IntegerField(blank=True, db_column='Цена', null=True)),
                ('валюта', models.CharField(blank=True, db_column='Валюта', max_length=3, null=True)),
                ('единица_измерения', models.CharField(blank=True, db_column='Единица_измерения', max_length=8, null=True)),
                ('минимальный_объем_заказа', models.DecimalField(blank=True, db_column='Минимальный_объем_заказа', decimal_places=3, max_digits=5, null=True)),
                ('оптовая_цена', models.DecimalField(blank=True, db_column='Оптовая_цена', decimal_places=5, max_digits=11, null=True)),
                ('минимальный_заказ_опт', models.DecimalField(blank=True, db_column='Минимальный_заказ_опт', decimal_places=3, max_digits=9, null=True)),
                ('ссылка_изображения', models.CharField(blank=True, db_column='Ссылка_изображения', max_length=828, null=True)),
                ('наличие', models.CharField(blank=True, db_column='Наличие', max_length=2, null=True)),
                ('количество', models.IntegerField(blank=True, db_column='Количество', null=True)),
                ('номер_группы', models.IntegerField(blank=True, db_column='Номер_группы', null=True)),
                ('название_группы', models.CharField(blank=True, db_column='Название_группы', max_length=100, null=True)),
                ('адрес_подраздела', models.CharField(blank=True, db_column='Адрес_подраздела', max_length=77, null=True)),
                ('возможность_поставки', models.IntegerField(blank=True, db_column='Возможность_поставки', null=True)),
                ('срок_поставки', models.CharField(blank=True, db_column='Срок_поставки', max_length=7, null=True)),
                ('способ_упаковки', models.CharField(blank=True, db_column='Способ_упаковки', max_length=40, null=True)),
                ('идентификатор_товара', models.CharField(blank=True, db_column='Идентификатор_товара', max_length=24, null=True)),
                ('идентификатор_подраздела', models.IntegerField(blank=True, db_column='Идентификатор_подраздела', null=True)),
                ('идентификатор_группы', models.CharField(blank=True, db_column='Идентификатор_группы', max_length=30, null=True)),
                ('производитель', models.CharField(blank=True, db_column='Производитель', max_length=11, null=True)),
                ('страна_производитель', models.CharField(blank=True, db_column='Страна_производитель', max_length=11, null=True)),
                ('скидка', models.CharField(blank=True, db_column='Скидка', max_length=30, null=True)),
                ('id_группы_разновидностей', models.CharField(blank=True, db_column='ID_группы_разновидностей', max_length=30, null=True)),
                ('личные_заметки', models.CharField(blank=True, db_column='Личные_заметки', max_length=30, null=True)),
                ('продукт_на_сайте', models.CharField(blank=True, db_column='Продукт_на_сайте', max_length=84, null=True)),
                ('cрок_действия_скидки_от', models.CharField(blank=True, db_column='Cрок_действия_скидки_от', max_length=30, null=True)),
                ('cрок_действия_скидки_до', models.CharField(blank=True, db_column='Cрок_действия_скидки_до', max_length=30, null=True)),
            ],
            options={
                'db_table': 'shop_product',
                'managed': False,
            },
        ),
    ]
