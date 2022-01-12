# Generated by Django 4.0 on 2022-01-12 23:01

from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(db_index=True, max_length=255, unique=True)),
                ('email', models.EmailField(db_index=True, max_length=255, unique=True)),
                ('otp', models.CharField(max_length=200)),
                ('is_verified', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
            managers=[
                ('object', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='AccountManager',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_type', models.CharField(choices=[('Savings account', 'Savings account'), ('Current Account', 'Current Account'), ('Fixed Account', 'Fixed Account')], max_length=250, null=True)),
                ('fullname', models.CharField(max_length=250, null=True)),
                ('gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Binary', 'Binary')], max_length=50, null=True)),
                ('phone_number', models.BigIntegerField(null=True)),
                ('address', models.TextField(max_length=255, null=True)),
                ('occupation', models.CharField(max_length=200, null=True)),
                ('account_number', models.IntegerField(null=True, unique=True)),
                ('user_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='webank.user')),
            ],
        ),
        migrations.CreateModel(
            name='Balance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_balance', models.DecimalField(decimal_places=2, max_digits=50)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webank.user')),
                ('customer_account', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='webank.accountmanager')),
            ],
        ),
        migrations.CreateModel(
            name='TransactionHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_time', models.DateTimeField(auto_now_add=True)),
                ('transaction_type', models.CharField(max_length=250)),
                ('transaction_amount', models.DecimalField(decimal_places=2, max_digits=50)),
                ('current_balance', models.DecimalField(decimal_places=2, default=0, max_digits=50)),
                ('account_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='webank.accountmanager')),
                ('balance_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='webank.balance')),
                ('user_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='webank.user')),
            ],
        ),
    ]
