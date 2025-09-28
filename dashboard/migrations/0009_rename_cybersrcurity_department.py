from django.db import migrations

OLD_NAME = 'Computer Science and Engineering ( IOT and Cybersrcurity)'
NEW_NAME = 'Computer Science and Engineering ( IOT and Cybersecurity)'


def rename_department(apps, schema_editor):
    Department = apps.get_model('dashboard', 'Department')
    try:
        dept = Department.objects.get(name=OLD_NAME)
        dept.name = NEW_NAME
        dept.save()
    except Department.DoesNotExist:
        # Already renamed or never existed; nothing to do
        pass


def reverse_noop(apps, schema_editor):
    # Do not revert automatically (to avoid reintroducing typo)
    pass

class Migration(migrations.Migration):
    dependencies = [
        ('dashboard', '0008_seed_core_departments'),
    ]

    operations = [
        migrations.RunPython(rename_department, reverse_noop)
    ]
