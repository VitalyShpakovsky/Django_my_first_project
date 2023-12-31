# Generated by Django 4.2.1 on 2023-06-29 17:37

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myauth', '0001_initial'),
        ('shopapp', '0006_alter_product_discount'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='created_by',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='myauth.profile'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='order',
            name='delivery_address',
            field=models.TextField(validators=[django.core.validators.RegexValidator(message="The field must contain word 'city'", regex='city')]),
        ),
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.TextField(blank=True, validators=[django.core.validators.RegexValidator(message="The field must contain words 'Made in'", regex='Made in')]),
        ),
    ]
