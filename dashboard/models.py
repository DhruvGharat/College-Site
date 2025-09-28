from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Faculty(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    employee_id = models.CharField(max_length=20, unique=True)
    department = models.ForeignKey('Department', on_delete=models.CASCADE)
    department_name = models.CharField(max_length=100)  # Added to match database schema
    designation = models.CharField(max_length=100)
    phone = models.CharField(max_length=15, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.employee_id})"


class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=10, unique=True)
    
    def __str__(self):
        return self.name


class Subject(models.Model):
    SCHEME_CHOICES = [
        ('R19-20', 'R19-20'),
        ('NEP', 'NEP'),
        ('AUTONOMOUS', 'Autonomous'),
    ]
    
    YEAR_CHOICES = [
        (1, '1st Year'),
        (2, '2nd Year'),
        (3, '3rd Year'),
        (4, '4th Year'),
    ]
    
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=20)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    year = models.IntegerField(choices=YEAR_CHOICES)
    scheme = models.CharField(max_length=20, choices=SCHEME_CHOICES)
    credits = models.IntegerField(default=3)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, null=True, blank=True)
    # New optional academic session range e.g. "2005-2006" if provided via UI
    academic_year = models.CharField(max_length=9, blank=True, help_text="Academic session like 2005-2006")
    
    class Meta:
        # Removed unique_together constraint to allow duplicate subject codes
        pass
    
    def __str__(self):
        return f"{self.name} ({self.code}) - {self.display_year}"

    @property
    def display_year(self):
        """Return academic_year range if set, else the standard year display.

        This lets templates uniformly reference s.display_year and get either
        the custom academic session (e.g. 2010-2011) or the ordinal year label
        (e.g. 1st Year) when no range was captured.
        """
        if self.academic_year:
            return self.academic_year
        # Fallback to Django's choice display for the numeric year
        return self.get_year_display()


class Student(models.Model):
    roll_number = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=200)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    year = models.IntegerField(choices=Subject.YEAR_CHOICES)
    scheme = models.CharField(max_length=20, choices=Subject.SCHEME_CHOICES)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=15, blank=True)
    
    def __str__(self):
        return f"{self.name} ({self.roll_number})"


class Result(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    marks_obtained = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    total_marks = models.IntegerField(default=100)
    exam_type = models.CharField(max_length=50, default='Mid Term')
    semester = models.CharField(max_length=20, default='1st')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    @property
    def status(self):
        return 'Pass' if self.marks_obtained >= 40 else 'Fail'
    
    @property
    def percentage(self):
        return round((self.marks_obtained / self.total_marks) * 100, 2)
    
    class Meta:
        unique_together = ['student', 'subject', 'exam_type', 'semester']
    
    def __str__(self):
        return f"{self.student.name} - {self.subject.name}: {self.marks_obtained}"


class COPO(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    co_number = models.CharField(max_length=10)  # CO1, CO2, etc.
    co_description = models.TextField()
    po_mapping = models.JSONField(default=dict)  # Store PO mappings as JSON
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['subject', 'co_number']
    
    def __str__(self):
        return f"{self.subject.code} - {self.co_number}"


class FacultySelection(models.Model):
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    year = models.IntegerField(choices=Subject.YEAR_CHOICES)
    scheme = models.CharField(max_length=20, choices=Subject.SCHEME_CHOICES)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['faculty', 'year', 'scheme', 'department']
    
    def __str__(self):
        return f"{self.faculty.user.get_full_name()} - {self.get_year_display()} {self.scheme}"


class PredefinedSubject(models.Model):
    """Stores predefined subject names per department so UI can populate dynamically."""
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='predefined_subjects')
    name = models.CharField(max_length=200)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['department', 'name']
        ordering = ['name']

    def __str__(self):
        return f"{self.department.name} - {self.name}"