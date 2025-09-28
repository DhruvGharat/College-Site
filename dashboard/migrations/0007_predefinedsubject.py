from django.db import migrations, models

IT_SUBJECTS = [
    'Software Engineering',
    'Computer Network Security',
    'Entrepreneurship and E-Business',
    'Advanced Data Structures',
    'ADMT',
    'Internet Programming'
    'Web Technologies',
]

ALLOWED_DEPARTMENTS = [
    'Information Technology',
    'Electronics and telecommunication',
    'Computer Engineering',
    'Computer Science and Engineering ( IOT and Cybersecurity)'
]

def seed_it_subjects(apps, schema_editor):
    Department = apps.get_model('dashboard', 'Department')
    PredefinedSubject = apps.get_model('dashboard', 'PredefinedSubject')
    # Create predefined subjects only for Information Technology
    try:
        it_dept = Department.objects.get(name='Information Technology')
    except Department.DoesNotExist:
        return
    for name in IT_SUBJECTS:
        PredefinedSubject.objects.get_or_create(department=it_dept, name=name)


def remove_it_subjects(apps, schema_editor):
    PredefinedSubject = apps.get_model('dashboard', 'PredefinedSubject')
    PredefinedSubject.objects.filter(name__in=IT_SUBJECTS).delete()

class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0006_subject_academic_year'),
    ]

    operations = [
        migrations.CreateModel(
            name='PredefinedSubject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('department', models.ForeignKey(on_delete=models.deletion.CASCADE, related_name='predefined_subjects', to='dashboard.department')),
            ],
            options={
                'ordering': ['name'],
                'unique_together': {('department', 'name')},
            },
        ),
        migrations.RunPython(seed_it_subjects, remove_it_subjects),
    ]
