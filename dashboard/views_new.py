from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Max, Min, Count
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import Faculty, Subject, Result
import logging

logger = logging.getLogger(__name__)

@login_required
@require_http_methods(["GET"])
def results_analytics_api(request):
    """
    API endpoint to get comprehensive results analytics.
    Returns statistics about student results for the faculty's subjects.
    """
    try:
        logger.info(f"Starting results_analytics_api for user: {request.user.username}")
        
        # Get faculty profile
        faculty = Faculty.objects.filter(user=request.user).first()
        if not faculty:
            logger.error(f"Faculty profile not found for user {request.user.id}")
            return JsonResponse({'error': 'Faculty profile not found.'}, status=400)
            
        logger.info(f"Found faculty: {faculty}")
        
        # Get selected subject or all subjects for the faculty's department
        selected_subject_id = request.session.get('selected_subject')
        logger.info(f"Selected subject ID from session: {selected_subject_id}")
        
        if selected_subject_id:
            subjects = Subject.objects.filter(id=selected_subject_id)
            logger.info(f"Filtering by selected subject ID: {selected_subject_id}")
        else:
            logger.info(f"Getting all subjects for department: {faculty.department}")
            subjects = Subject.objects.filter(department=faculty.department)
        
        logger.info(f"Found {subjects.count()} subjects")
        
        if not subjects.exists():
            logger.warning("No subjects found for the selected criteria")
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
        logger.info(f"Found {results.count()} results for the subjects")
        
        if not results.exists():
            logger.info("No results found for the selected subjects")
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
        fail_count = total_students - pass_count
        
        # Get aggregates
        aggregates = results.aggregate(
            avg=Avg('marks_obtained'),
            max=Max('marks_obtained'),
            min=Min('marks_obtained')
        )
        
        average_marks = round(aggregates['avg'], 2) if aggregates['avg'] is not None else 0
        highest_marks = aggregates['max'] if aggregates['max'] is not None else 0
        lowest_marks = aggregates['min'] if aggregates['min'] is not None else 0
        
        # Per-course breakdown
        per_course_breakdown = []
        for subject in subjects:
            subject_results = results.filter(subject=subject)
            if subject_results.exists():
                subject_agg = subject_results.aggregate(
                    total=Count('id'),
                    avg=Avg('marks_obtained'),
                    max=Max('marks_obtained'),
                    min=Min('marks_obtained')
                )
                subject_pass_count = subject_results.filter(marks_obtained__gte=40).count()
                
                per_course_breakdown.append({
                    'course_code': subject.code,
                    'course_name': subject.name,
                    'total_students': subject_agg['total'],
                    'average_marks': round(subject_agg['avg'], 2) if subject_agg['avg'] is not None else 0,
                    'highest_marks': subject_agg['max'] if subject_agg['max'] is not None else 0,
                    'lowest_marks': subject_agg['min'] if subject_agg['min'] is not None else 0,
                    'pass_count': subject_pass_count,
                    'fail_count': subject_agg['total'] - subject_pass_count,
                    'pass_percentage': round((subject_pass_count / subject_agg['total']) * 100, 2) if subject_agg['total'] > 0 else 0
                })
        
        # Student-wise results
        student_results = []
        for result in results:
            student_results.append({
                'roll_no': result.student.roll_number,
                'name': result.student.name,
                'course_code': result.subject.code,
                'course_name': result.subject.name,
                'marks': result.marks_obtained,
                'status': 'Pass' if result.marks_obtained >= 40 else 'Fail',
                'percentage': result.percentage
            })
        
        # Prepare response
        response_data = {
            'total_students': total_students,
            'pass_count': pass_count,
            'fail_count': fail_count,
            'average_marks': average_marks,
            'highest_marks': highest_marks,
            'lowest_marks': lowest_marks,
            'pass_percentage': round((pass_count / total_students) * 100, 2) if total_students > 0 else 0,
            'per_course_breakdown': per_course_breakdown,
            'student_results': student_results
        }
        
        logger.info("Successfully prepared analytics data")
        return JsonResponse(response_data)
        
    except Exception as e:
        logger.error(f"Error in results_analytics_api: {str(e)}", exc_info=True)
        return JsonResponse({'error': 'An error occurred while processing your request.'}, status=500)
