# Generated by Django 4.1.7 on 2023-03-06 17:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_alter_patient_options_customer_created_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('doc_name', models.CharField(max_length=150)),
                ('doc_email', models.EmailField(blank=True, max_length=254, null=True)),
                ('mobile', models.CharField(max_length=20)),
                ('job_title', models.CharField(max_length=150)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ('-created',),
            },
        ),
        migrations.AlterModelOptions(
            name='customer',
            options={'ordering': ('-created',), 'verbose_name': 'Accounts', 'verbose_name_plural': 'Accounts'},
        ),
        migrations.AddField(
            model_name='patient',
            name='doctor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='patient', to='account.doctor'),
        ),
    ]
