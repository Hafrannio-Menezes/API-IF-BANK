# gerado pelo django 5.2.7 em 2026-03-19 17:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FinancialGoal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=150)),
                ('target_amount', models.DecimalField(decimal_places=2, max_digits=14)),
                ('current_amount', models.DecimalField(decimal_places=2, default=0, max_digits=14)),
                ('deadline', models.DateField()),
                ('status', models.CharField(choices=[('ACTIVE', 'Active'), ('ACHIEVED', 'Achieved'), ('CANCELLED', 'Cancelled')], default='ACTIVE', max_length=15)),
            ],
            options={
                'verbose_name': 'Financial goal',
                'verbose_name_plural': 'Financial goals',
                'ordering': ['deadline', '-created_at'],
            },
        ),
    ]
