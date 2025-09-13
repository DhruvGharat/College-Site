from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from dashboard.models import Faculty, Department, Subject, Student, Result


class Command(BaseCommand):
    help = 'Populate the database with initial data'

    def handle(self, *args, **options):
        self.stdout.write('Creating initial data...')
        
        # Create departments
        departments_data = [
            {'name': 'Computer Science and Engineering', 'code': 'CSE'},
            {'name': 'Information Technology', 'code': 'IT'},
            {'name': 'Electronics and Communication Engineering', 'code': 'ECE'},
            {'name': 'Mechanical Engineering', 'code': 'ME'},
            {'name': 'Civil Engineering', 'code': 'CE'},
        ]
        
        departments = {}
        for dept_data in departments_data:
            dept, created = Department.objects.get_or_create(
                code=dept_data['code'],
                defaults={'name': dept_data['name']}
            )
            departments[dept_data['code']] = dept
            if created:
                self.stdout.write(f'Created department: {dept.name}')
        
        # Create faculty users
        faculty_data = [
            {
                'username': 'faculty1',
                'email': 'faculty1@college.edu',
                'first_name': 'John',
                'last_name': 'Smith',
                'employee_id': 'EMP001',
                'department': 'CSE',
                'designation': 'Assistant Professor'
            },
            {
                'username': 'faculty2',
                'email': 'faculty2@college.edu',
                'first_name': 'Jane',
                'last_name': 'Doe',
                'employee_id': 'EMP002',
                'department': 'IT',
                'designation': 'Associate Professor'
            },
            {
                'username': 'faculty3',
                'email': 'faculty3@college.edu',
                'first_name': 'Bob',
                'last_name': 'Johnson',
                'employee_id': 'EMP003',
                'department': 'ECE',
                'designation': 'Professor'
            }
        ]
        
        for faculty_info in faculty_data:
            user, created = User.objects.get_or_create(
                username=faculty_info['username'],
                defaults={
                    'email': faculty_info['email'],
                    'first_name': faculty_info['first_name'],
                    'last_name': faculty_info['last_name'],
                }
            )
            
            if created:
                user.set_password('password123')  # Default password
                user.save()
                self.stdout.write(f'Created user: {user.username}')
            
            faculty, created = Faculty.objects.get_or_create(
                user=user,
                defaults={
                    'employee_id': faculty_info['employee_id'],
                    'department': faculty_info['department'],
                    'designation': faculty_info['designation'],
                }
            )
            
            if created:
                self.stdout.write(f'Created faculty: {faculty.user.get_full_name()}')
        
        # Create subjects
        subjects_data = [
            {
                'name': 'Data Structures and Algorithms',
                'code': 'CS201',
                'department': 'CSE',
                'year': 2,
                'scheme': 'R19-20',
                'credits': 4
            },
            {
                'name': 'Database Management Systems',
                'code': 'CS301',
                'department': 'CSE',
                'year': 3,
                'scheme': 'R19-20',
                'credits': 4
            },
            {
                'name': 'Web Technologies',
                'code': 'IT301',
                'department': 'IT',
                'year': 3,
                'scheme': 'R19-20',
                'credits': 3
            },
            {
                'name': 'Digital Electronics',
                'code': 'EC201',
                'department': 'ECE',
                'year': 2,
                'scheme': 'R19-20',
                'credits': 4
            }
        ]
        
        subjects = {}
        for subject_data in subjects_data:
            subject, created = Subject.objects.get_or_create(
                code=subject_data['code'],
                year=subject_data['year'],
                scheme=subject_data['scheme'],
                defaults={
                    'name': subject_data['name'],
                    'department': departments[subject_data['department']],
                    'credits': subject_data['credits']
                }
            )
            subjects[subject_data['code']] = subject
            if created:
                self.stdout.write(f'Created subject: {subject.name}')
        
        # Create sample students
        students_data = [
            {'roll_number': '21CS001', 'name': 'Alice Johnson', 'department': 'CSE', 'year': 2, 'scheme': 'R19-20'},
            {'roll_number': '21CS002', 'name': 'Bob Smith', 'department': 'CSE', 'year': 2, 'scheme': 'R19-20'},
            {'roll_number': '21CS003', 'name': 'Charlie Brown', 'department': 'CSE', 'year': 2, 'scheme': 'R19-20'},
            {'roll_number': '21CS004', 'name': 'Diana Prince', 'department': 'CSE', 'year': 2, 'scheme': 'R19-20'},
            {'roll_number': '21CS005', 'name': 'Eve Wilson', 'department': 'CSE', 'year': 2, 'scheme': 'R19-20'},
            {'roll_number': '21IT001', 'name': 'Frank Miller', 'department': 'IT', 'year': 3, 'scheme': 'R19-20'},
            {'roll_number': '21IT002', 'name': 'Grace Lee', 'department': 'IT', 'year': 3, 'scheme': 'R19-20'},
            {'roll_number': '21IT003', 'name': 'Henry Davis', 'department': 'IT', 'year': 3, 'scheme': 'R19-20'},
        ]
        
        students = {}
        for student_data in students_data:
            student, created = Student.objects.get_or_create(
                roll_number=student_data['roll_number'],
                defaults={
                    'name': student_data['name'],
                    'department': departments[student_data['department']],
                    'year': student_data['year'],
                    'scheme': student_data['scheme']
                }
            )
            students[student_data['roll_number']] = student
            if created:
                self.stdout.write(f'Created student: {student.name}')
        
        # Create sample results
        import random
        
        # Results for CS201 (Data Structures)
        cs201_students = [s for s in students.values() if s.department.code == 'CSE' and s.year == 2]
        for student in cs201_students:
            marks = random.randint(35, 95)
            result, created = Result.objects.get_or_create(
                student=student,
                subject=subjects['CS201'],
                exam_type='Mid Term',
                semester='1st',
                defaults={'marks_obtained': marks}
            )
            if created:
                self.stdout.write(f'Created result for {student.name}: {marks} marks')
        
        # Results for IT301 (Web Technologies)
        it301_students = [s for s in students.values() if s.department.code == 'IT' and s.year == 3]
        for student in it301_students:
            marks = random.randint(40, 90)
            result, created = Result.objects.get_or_create(
                student=student,
                subject=subjects['IT301'],
                exam_type='Mid Term',
                semester='1st',
                defaults={'marks_obtained': marks}
            )
            if created:
                self.stdout.write(f'Created result for {student.name}: {marks} marks')
        
        self.stdout.write(
            self.style.SUCCESS('Successfully populated database with initial data!')
        )
        self.stdout.write('\nDefault login credentials:')
        self.stdout.write('Username: faculty1, Password: password123')
        self.stdout.write('Username: faculty2, Password: password123')
        self.stdout.write('Username: faculty3, Password: password123')
