# Generated by Django 4.1.7 on 2023-03-08 14:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0013_prescription_payment'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='amount',
            field=models.DecimalField(decimal_places=2, default=100, max_digits=10),
            preserve_default=False,
        ),
    ]
