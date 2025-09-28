from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0005_alter_faculty_department_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='subject',
            name='academic_year',
            field=models.CharField(blank=True, help_text='Academic session like 2005-2006', max_length=9),
        ),
    ]
