# gerado pelo django 5.2.7 em 2026-03-19 17:54

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='bankaccount',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='accounts', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddConstraint(
            model_name='bankaccount',
            constraint=models.CheckConstraint(condition=models.Q(('balance__gte', 0)), name='accounts_balance_non_negative'),
        ),
    ]
