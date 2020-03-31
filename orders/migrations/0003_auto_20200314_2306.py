# Generated by Django 3.0.2 on 2020-03-14 22:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0003_auto_20200314_2143'),
        ('orders', '0002_auto_20200313_2152'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='activate',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='order',
            name='billing_profile',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='billing.BillingProfile'),
        ),
    ]
