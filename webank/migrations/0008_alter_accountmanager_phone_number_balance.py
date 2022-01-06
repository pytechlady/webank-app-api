# Generated by Django 4.0 on 2022-01-06 12:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('webank', '0007_alter_accountmanager_account_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accountmanager',
            name='phone_number',
            field=models.BigIntegerField(null=True),
        ),
        migrations.CreateModel(
            name='Balance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_balance', models.DecimalField(decimal_places=2, max_digits=10)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webank.accountmanager')),
            ],
        ),
    ]
