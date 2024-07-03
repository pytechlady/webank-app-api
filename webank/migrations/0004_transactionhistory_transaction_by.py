# Generated by Django 4.0.10 on 2024-07-03 15:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('webank', '0003_accountmanager_created_at_accountmanager_updated_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='transactionhistory',
            name='transaction_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='transaction_manager', to=settings.AUTH_USER_MODEL),
        ),
    ]
