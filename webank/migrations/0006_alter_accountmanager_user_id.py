# Generated by Django 4.0 on 2022-01-05 10:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('webank', '0005_accountmanager_fullname'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accountmanager',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webank.user', unique=True),
        ),
    ]