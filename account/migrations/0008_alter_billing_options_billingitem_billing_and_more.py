# Generated by Django 4.1.7 on 2023-03-07 15:53

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0007_billing_created'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='billing',
            options={'ordering': ('-created',)},
        ),
        migrations.AddField(
            model_name='billingitem',
            name='billing',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='billing_items', to='account.billing'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='billingitem',
            name='bill_qty',
            field=models.CharField(default=1, max_length=30),
        ),
    ]
