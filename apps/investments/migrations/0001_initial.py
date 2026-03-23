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
            name='InvestmentProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=150, unique=True)),
                ('product_type', models.CharField(choices=[('CDB', 'CDB'), ('CDI_FUND', 'CDI Fund'), ('TESOURO', 'Tesouro Direto'), ('LCI', 'LCI'), ('FIXED_INCOME', 'Fixed Income')], max_length=20)),
                ('annual_rate', models.DecimalField(decimal_places=4, max_digits=7)),
                ('minimum_initial_amount', models.DecimalField(decimal_places=2, max_digits=14)),
                ('term_days', models.PositiveIntegerField(default=30)),
                ('risk_level', models.CharField(choices=[('LOW', 'Low'), ('MEDIUM', 'Medium'), ('HIGH', 'High')], max_length=10)),
                ('description', models.TextField(blank=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Investment product',
                'verbose_name_plural': 'Investment products',
                'ordering': ['name'],
                'constraints': [models.CheckConstraint(condition=models.Q(('annual_rate__gte', 0)), name='investments_product_annual_rate_non_negative'), models.CheckConstraint(condition=models.Q(('minimum_initial_amount__gt', 0)), name='investments_product_minimum_initial_amount_positive')],
            },
        ),
        migrations.CreateModel(
            name='PortfolioPosition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('invested_amount', models.DecimalField(decimal_places=2, default=0, max_digits=14)),
                ('current_balance', models.DecimalField(decimal_places=2, default=0, max_digits=14)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='portfolio_positions', to='accounts.bankaccount')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='positions', to='investments.investmentproduct')),
            ],
            options={
                'verbose_name': 'Portfolio position',
                'verbose_name_plural': 'Portfolio positions',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='InvestmentTransaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_type', models.CharField(choices=[('APPLY', 'Apply'), ('REDEEM', 'Redeem')], max_length=10)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=14)),
                ('reference_code', models.CharField(max_length=25, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('position', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='investment_transactions', to='investments.portfolioposition')),
            ],
            options={
                'verbose_name': 'Investment transaction',
                'verbose_name_plural': 'Investment transactions',
                'ordering': ['-created_at'],
            },
        ),
        migrations.AddConstraint(
            model_name='portfolioposition',
            constraint=models.UniqueConstraint(fields=('account', 'product'), name='unique_portfolio_position'),
        ),
        migrations.AddConstraint(
            model_name='portfolioposition',
            constraint=models.CheckConstraint(condition=models.Q(('invested_amount__gte', 0)), name='portfolio_invested_amount_non_negative'),
        ),
        migrations.AddConstraint(
            model_name='portfolioposition',
            constraint=models.CheckConstraint(condition=models.Q(('current_balance__gte', 0)), name='portfolio_current_balance_non_negative'),
        ),
        migrations.AddConstraint(
            model_name='investmenttransaction',
            constraint=models.CheckConstraint(condition=models.Q(('amount__gt', 0)), name='investment_transaction_amount_positive'),
        ),
    ]
