# gerado pelo django 5.2.7 em 2026-03-19 17:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_type', models.CharField(choices=[('DEPOSIT', 'Deposit'), ('WITHDRAWAL', 'Withdrawal'), ('TRANSFER_OUT', 'Transfer Out'), ('TRANSFER_IN', 'Transfer In')], max_length=20)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=14)),
                ('description', models.CharField(blank=True, max_length=255)),
                ('status', models.CharField(choices=[('COMPLETED', 'Completed'), ('FAILED', 'Failed')], max_length=20)),
                ('reference_code', models.CharField(max_length=25, unique=True)),
                ('balance_after', models.DecimalField(decimal_places=2, max_digits=14)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to='accounts.bankaccount')),
                ('destination_account', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='incoming_transfer_references', to='accounts.bankaccount')),
            ],
            options={
                'verbose_name': 'Transaction',
                'verbose_name_plural': 'Transactions',
                'ordering': ['-created_at'],
                'constraints': [models.CheckConstraint(condition=models.Q(('amount__gt', 0)), name='transactions_amount_positive'), models.CheckConstraint(condition=models.Q(('balance_after__gte', 0)), name='transactions_balance_after_non_negative')],
            },
        ),
    ]
