from django.db import migrations


def noop(*args, **kwargs):
    return None


class Migration(migrations.Migration):
    dependencies = [
        ("investments", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(noop, reverse_code=noop),
    ]
