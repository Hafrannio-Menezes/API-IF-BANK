# gerado pelo django 5.2.7 em 2026-03-19 17:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BankAccount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('account_number', models.CharField(max_length=20, unique=True)),
                ('agency_number', models.CharField(max_length=10)),
                ('account_type', models.CharField(choices=[('CHECKING', 'Checking'), ('SAVINGS', 'Savings'), ('INVESTMENT', 'Investment')], max_length=20)),
                ('balance', models.DecimalField(decimal_places=2, default=0, max_digits=14)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Bank account',
                'verbose_name_plural': 'Bank accounts',
                'ordering': ['-created_at'],
            },
        ),
    ]
