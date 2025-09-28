from django.db import migrations

DEPARTMENTS = [
    ('Information Technology', 'IT'),
    ('Electronics and telecommunication', 'ENTC'),
    ('Computer Engineering', 'COMP'),
    ('Computer Science and Engineering ( IOT and Cybersecurity)', 'CSE-IOT-CS')
]

def seed_departments(apps, schema_editor):
    Department = apps.get_model('dashboard', 'Department')
    for name, code in DEPARTMENTS:
        Department.objects.get_or_create(name=name, defaults={'code': code})

def unseed_departments(apps, schema_editor):
    # Don't delete on reverse to avoid removing real data
    pass

class Migration(migrations.Migration):
    dependencies = [
        ('dashboard', '0007_predefinedsubject'),
    ]

    operations = [
        migrations.RunPython(seed_departments, unseed_departments)
    ]
