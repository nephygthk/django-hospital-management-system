# Generated by Django 4.1.7 on 2023-03-10 15:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0020_alter_payment_receipt'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='billing',
            name='balance',
        ),
        migrations.AddField(
            model_name='billing',
            name='billing_receipt',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]
