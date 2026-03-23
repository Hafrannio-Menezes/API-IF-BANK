# gerado pelo django 5.2.7 em 2026-03-19 17:54

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('goals', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='financialgoal',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='financial_goals', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddConstraint(
            model_name='financialgoal',
            constraint=models.CheckConstraint(condition=models.Q(('target_amount__gt', 0)), name='goals_target_amount_positive'),
        ),
        migrations.AddConstraint(
            model_name='financialgoal',
            constraint=models.CheckConstraint(condition=models.Q(('current_amount__gte', 0)), name='goals_current_amount_non_negative'),
        ),
    ]
