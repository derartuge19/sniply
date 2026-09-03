from django.db import migrations


def create_plans(apps, schema_editor):
    Plan = apps.get_model("billing", "Plan")
    Plan.objects.create(name="Free", link_limit=100, custom_domain_allowed=False, price=0)
    Plan.objects.create(name="Pro", link_limit=None, custom_domain_allowed=True, price=9.00)


def delete_plans(apps, schema_editor):
    Plan = apps.get_model("billing", "Plan")
    Plan.objects.filter(name__in=["Free", "Pro"]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("billing", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(create_plans, delete_plans),
    ]