from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from django.db.models import Avg, Max, Min, Count
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from .models import Faculty, Department, Subject, Student, Result, FacultySelection
from .forms import FacultyLoginForm, FacultySelectionForm


def login_view(request):
    if request.user.is_authenticated:
        return redirect('selection')
    
    if request.method == 'POST':
        print(f"POST request received: {request.POST}")  # Debug
        
        # Try direct authentication first (bypass form validation)
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(f"Direct auth attempt: username='{username}', password='{password}'")  # Debug
        
        if username and password:
            user = authenticate(request, username=username, password=password)
            print(f"User authenticated: {user}")  # Debug
            
            if user is not None:
                try:
                    faculty = Faculty.objects.get(user=user)
                    print(f"Faculty found: {faculty}")  # Debug
                    login(request, user)
                    print("Login successful, redirecting to selection")  # Debug
                    return redirect('selection')
                except Faculty.DoesNotExist:
                    print("Faculty.DoesNotExist error")  # Debug
                    messages.error(request, 'Access denied. Faculty account required.')
            else:
                print("Authentication failed")  # Debug
                messages.error(request, 'Invalid username or password.')
        else:
            print("Missing username or password")  # Debug
            messages.error(request, 'Please enter both username and password.')
        
        # Also try form validation for debugging
        form = FacultyLoginForm(request.POST)
        print(f"Form is valid: {form.is_valid()}")  # Debug
        if not form.is_valid():
            print(f"Form errors: {form.errors}")  # Debug
    else:
        form = FacultyLoginForm()
    
    return render(request, 'dashboard/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def selection_view(request):
    try:
        faculty = Faculty.objects.get(user=request.user)
    except Faculty.DoesNotExist:
        messages.error(request, 'Faculty profile not found.')
        return redirect('login')
    
    if request.method == 'POST':
        form = FacultySelectionForm(request.POST)
        if form.is_valid():
            year = form.cleaned_data['year']
            scheme = form.cleaned_data['scheme']
            department = form.cleaned_data['department']
            subject = form.cleaned_data.get('subject')
            
            # Save selection in session
            request.session['selected_year'] = year
            request.session['selected_scheme'] = scheme
            request.session['selected_department'] = department.id
            request.session['selected_subject'] = subject.id if subject else None
            
            # Save or update FacultySelection
            selection, created = FacultySelection.objects.get_or_create(
                faculty=faculty,
                year=year,
                scheme=scheme,
                department=department,
                defaults={'subject': subject}
            )
            if not created:
                selection.subject = subject
                selection.save()
            
            return redirect('dashboard')
    else:
        form = FacultySelectionForm()
    
    return render(request, 'dashboard/selection.html', {'form': form, 'faculty': faculty})


@login_required
def dashboard_view(request):
    try:
        faculty = Faculty.objects.get(user=request.user)
    except Faculty.DoesNotExist:
        messages.error(request, 'Faculty profile not found.')
        return redirect('login')
    
    # Get session data
    selected_year = request.session.get('selected_year')
    selected_scheme = request.session.get('selected_scheme')
    selected_department_id = request.session.get('selected_department')
    selected_subject_id = request.session.get('selected_subject')
    
    context = {
        'faculty': faculty,
        'selected_year': selected_year,
        'selected_scheme': selected_scheme,
        'selected_department': Department.objects.get(id=selected_department_id) if selected_department_id else None,
        'selected_subject': Subject.objects.get(id=selected_subject_id) if selected_subject_id else None,
    }
    
    return render(request, 'dashboard/dashboard.html', context)


@login_required
def home_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
        
    try:
        faculty = Faculty.objects.get(user=request.user)
    except Faculty.DoesNotExist:
        messages.error(request, 'Faculty profile not found.')
        return redirect('login')
    
    # Get session data
    selected_year = request.session.get('selected_year')
    selected_scheme = request.session.get('selected_scheme')
    selected_department_id = request.session.get('selected_department')
    selected_subject_id = request.session.get('selected_subject')
    
    # Motivational quotes
    quotes = [
        "Education is the most powerful weapon which you can use to change the world. - Nelson Mandela",
        "The future belongs to those who believe in the beauty of their dreams. - Eleanor Roosevelt",
        "Success is not final, failure is not fatal: it is the courage to continue that counts. - Winston Churchill",
        "The only way to do great work is to love what you do. - Steve Jobs",
        "Innovation distinguishes between a leader and a follower. - Steve Jobs"
    ]
    
    import random
    daily_quote = random.choice(quotes)
    
    context = {
        'faculty': faculty,
        'selected_year': selected_year,
        'selected_scheme': selected_scheme,
        'selected_department': Department.objects.get(id=selected_department_id) if selected_department_id else None,
        'selected_subject': Subject.objects.get(id=selected_subject_id) if selected_subject_id else None,
        'daily_quote': daily_quote,
    }
    
    return render(request, 'dashboard/home.html', context)


@login_required
def results_view(request):
    """Results Dashboard - Main results page with analytics and upload functionality"""
    try:
        faculty = Faculty.objects.get(user=request.user)
    except Faculty.DoesNotExist:
        messages.error(request, 'Faculty profile not found.')
        return redirect('login')
    
    # Get session data
    selected_subject_id = request.session.get('selected_subject')
    selected_department_id = request.session.get('selected_department')
    
    context = {
        'faculty': faculty,
        'selected_subject': Subject.objects.get(id=selected_subject_id) if selected_subject_id else None,
        'selected_department': Department.objects.get(id=selected_department_id) if selected_department_id else None,
    }
    
    return render(request, 'dashboard/results_dashboard.html', context)


# Placeholder views for other tabs
@login_required
def goal_set_view(request):
    return render(request, 'dashboard/coming_soon.html', {'title': 'Goal Set'})

@login_required
def tool_assignment_view(request):
    return render(request, 'dashboard/coming_soon.html', {'title': 'Tool Assignment'})

@login_required
def marks_entry_view(request):
    return render(request, 'dashboard/coming_soon.html', {'title': 'Marks Entry'})

@login_required
def co_attainment_view(request):
    return render(request, 'dashboard/coming_soon.html', {'title': 'CO Attainment'})

@login_required
def co_po_mapping_view(request):
    return render(request, 'dashboard/coming_soon.html', {'title': 'CO-PO Mapping'})


@login_required
@require_http_methods(["GET"])
def download_excel_template(request):
    """Download Excel template for results upload"""
    try:
        # Create a new workbook
        wb = Workbook()
        ws = wb.active
        ws.title = "Results Template"
        
        # Define headers
        headers = ['Roll No', 'Name', 'Course Code', 'Marks']
        
        # Style for headers
        header_font = Font(bold=True, color="FFFFFF")
        header_fill = PatternFill(start_color="366092", end_color="366092", fill_type="solid")
        header_alignment = Alignment(horizontal="center", vertical="center")
        
        # Add headers
        for col, header in enumerate(headers, 1):
            cell = ws.cell(row=1, column=col, value=header)
            cell.font = header_font
            cell.fill = header_fill
            cell.alignment = header_alignment
        
        # Add sample data
        sample_data = [
            ['21CS001', 'John Doe', 'CS201', 85],
            ['21CS002', 'Jane Smith', 'CS201', 92],
            ['21CS003', 'Bob Johnson', 'CS201', 78],
            ['21CS004', 'Alice Brown', 'CS201', 65],
            ['21CS005', 'Charlie Wilson', 'CS201', 88]
        ]
        
        for row, data in enumerate(sample_data, 2):
            for col, value in enumerate(data, 1):
                ws.cell(row=row, column=col, value=value)
        
        # Auto-adjust column widths
        for column in ws.columns:
            max_length = 0
            column_letter = column[0].column_letter
            for cell in column:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                except:
                    pass
            adjusted_width = min(max_length + 2, 20)
            ws.column_dimensions[column_letter].width = adjusted_width
        
        # Create response
        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename="results_template.xlsx"'
        
        # Save workbook to response
        wb.save(response)
        return response
        
    except Exception as e:
        return JsonResponse({'error': f'Error creating template: {str(e)}'}, status=500)


@login_required
@require_http_methods(["POST"])
def upload_excel_results(request):
    """Upload and parse Excel file with results"""
    try:
        faculty = Faculty.objects.get(user=request.user)
    except Faculty.DoesNotExist:
        return JsonResponse({'error': 'Faculty profile not found.'}, status=400)
    
    if 'excel_file' not in request.FILES:
        return JsonResponse({'error': 'No file uploaded.'}, status=400)
    
    excel_file = request.FILES['excel_file']
    
    try:
        # Read Excel file using openpyxl
        from openpyxl import load_workbook
        wb = load_workbook(excel_file)
        ws = wb.active
        
        # Get headers from first row
        headers = []
        for cell in ws[1]:
            headers.append(cell.value)
        
        # Validate headers
        required_headers = ['Roll No', 'Name', 'Course Code', 'Marks']
        if not all(header in headers for header in required_headers):
            return JsonResponse({
                'error': f'Excel file must contain columns: {", ".join(required_headers)}'
            }, status=400)
        
        # Get column indices
        roll_no_idx = headers.index('Roll No')
        name_idx = headers.index('Name')
        course_code_idx = headers.index('Course Code')
        marks_idx = headers.index('Marks')
        
        # Process data
        created_count = 0
        updated_count = 0
        errors = []
        
        for row_num, row in enumerate(ws.iter_rows(min_row=2, values_only=True), 2):
            try:
                roll_no = str(row[roll_no_idx]).strip() if row[roll_no_idx] else None
                name = str(row[name_idx]).strip() if row[name_idx] else None
                course_code = str(row[course_code_idx]).strip() if row[course_code_idx] else None
                marks = int(row[marks_idx]) if row[marks_idx] else None
                
                if not all([roll_no, name, course_code, marks is not None]):
                    errors.append(f'Row {row_num}: Missing required data')
                    continue
                
                # Get or create student
                student, student_created = Student.objects.get_or_create(
                    roll_number=roll_no,
                    defaults={
                        'name': name,
                        'department': faculty.department,
                        'year': 2,  # Default year, can be made dynamic
                        'scheme': 'R19-20'  # Default scheme
                    }
                )
                
                # Get subject
                try:
                    subject = Subject.objects.get(code=course_code)
                except Subject.DoesNotExist:
                    errors.append(f'Row {row_num}: Course code "{course_code}" not found')
                    continue
                
                # Create or update result
                result, result_created = Result.objects.get_or_create(
                    student=student,
                    subject=subject,
                    exam_type='Mid Term',
                    semester='1st',
                    defaults={'marks_obtained': marks}
                )
                
                if not result_created:
                    result.marks_obtained = marks
                    result.save()
                    updated_count += 1
                else:
                    created_count += 1
                    
            except Exception as e:
                errors.append(f'Row {row_num}: {str(e)}')
                continue
        
        return JsonResponse({
            'success': True,
            'message': f'Successfully processed {created_count} new results and updated {updated_count} existing results.',
            'created': created_count,
            'updated': updated_count,
            'errors': errors[:10]  # Limit errors to first 10
        })
        
    except Exception as e:
        return JsonResponse({'error': f'Error processing Excel file: {str(e)}'}, status=400)


@login_required
@require_http_methods(["GET"])
def results_analytics_api(request):
    """Get comprehensive results analytics"""
    try:
        logger.info(f"Starting results_analytics_api for user: {request.user.username}")
        
        # Get faculty profile
        faculty = Faculty.objects.filter(user=request.user).first()
        if not faculty:
            logger.error(f"Faculty profile not found for user {request.user.id}")
            return JsonResponse({'error': 'Faculty profile not found.'}, status=400)
            
        # Get selected subject or all subjects for the faculty's department
        selected_subject_id = request.session.get('selected_subject')
        subjects = (Subject.objects.filter(id=selected_subject_id) if selected_subject_id 
                   else Subject.objects.filter(department=faculty.department))
        
        if not subjects.exists():
            return JsonResponse({
                'total_students': 0,
                'pass_count': 0,
                'fail_count': 0,
                'average_marks': 0,
                'highest_marks': 0,
                'lowest_marks': 0,
                'per_course_breakdown': [],
                'student_results': []
            })
            
        # Get results for the selected subjects
        results = Result.objects.filter(subject__in=subjects).select_related('student', 'subject')
        
        if not results.exists():
            return JsonResponse({
                'total_students': 0,
                'pass_count': 0,
                'fail_count': 0,
                'average_marks': 0,
                'highest_marks': 0,
                'lowest_marks': 0,
                'per_course_breakdown': [],
                'student_results': []
            })
            
        # Calculate overall statistics
        total_students = results.count()
        pass_count = results.filter(marks_obtained__gte=40).count()
        
        # Get aggregates
        aggregates = results.aggregate(
            avg=Avg('marks_obtained'),
            max=Max('marks_obtained'),
            min=Min('marks_obtained')
        )
        
        # Prepare response
        response_data = {
            'total_students': total_students,
            'pass_count': pass_count,
            'fail_count': total_students - pass_count,
            'average_marks': round(aggregates['avg'], 2) if aggregates['avg'] is not None else 0,
            'highest_marks': aggregates['max'] if aggregates['max'] is not None else 0,
            'lowest_marks': aggregates['min'] if aggregates['min'] is not None else 0,
            'pass_percentage': round((pass_count / total_students) * 100, 2) if total_students > 0 else 0,
            'per_course_breakdown': [],
            'student_results': [{
                'roll_no': r.student.roll_number,
                'name': r.student.name,
                'course_code': r.subject.code,
                'course_name': r.subject.name,
                'marks': r.marks_obtained,
                'status': 'Pass' if r.marks_obtained >= 40 else 'Fail',
                'percentage': r.percentage
            } for r in results]
        }
        
        return JsonResponse(response_data)
        
    except Exception as e:
        logger.error(f"Error in results_analytics_api: {str(e)}", exc_info=True)
        return JsonResponse({'error': 'An error occurred while processing your request.'}, status=500)