from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("investments", "0002_seed_products"),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name="portfolioposition",
            name="unique_portfolio_position",
        ),
    ]
