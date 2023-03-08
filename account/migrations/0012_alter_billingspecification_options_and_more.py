# Generated by Django 4.1.7 on 2023-03-08 11:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0011_alter_billing_patient'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='billingspecification',
            options={'ordering': ('-created',)},
        ),
        migrations.AlterField(
            model_name='billing',
            name='bill_amount',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]
