# Generated by Django 4.1.7 on 2023-03-07 14:12

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_billingspecification_billingitem'),
    ]

    operations = [
        migrations.AddField(
            model_name='billing',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]