from django.urls import path
from . import views

urlpatterns = [
    # Authentication
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    



    # Main pages
    path('selection/', views.selection_view, name='selection'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('dashboard/<int:subject_id>/', views.dashboard_view, name='dashboard_with_subject'),
    path('', views.home_view, name='home'),
    
    # Results Dashboard
    path('results/', views.results_view, name='results'),
    path('api/results/template/', views.download_excel_template, name='download_excel_template'),
    path('api/results/upload/', views.upload_excel_results, name='upload_excel_results'),
    path('api/results/analytics/', views.results_analytics_api, name='results_analytics'),
    path('api/results/download-analysis/', views.download_analysis_excel, name='download_analysis_excel'),
    path('api/results/download-students/', views.download_student_results, name='download_student_results'),
    path('api/results/remove/', views.remove_results_file, name='remove_results_file'),

    # Subjectspage
    path('subjectspage/', views.subjectspage_view, name='subjectspage'),
    path('subjectspage/add/', views.addsubjectpage_view, name='addsubjectpage'),
    path('subjectspage/<int:subject_id>/edit/', views.editsubjectpage_view, name='editsubjectpage'),
    path('subjectspage/<int:subject_id>/delete/', views.deletesubject_view, name='deletesubject'),

    # Other tabs (placeholder)
    path('goal-set/', views.goal_set_view, name='goal_set'),
    path('tool-assignment/', views.tool_assignment_view, name='tool_assignment'),
    path('marks-entry/', views.marks_entry_view, name='marks_entry'),
    path('co-attainment/', views.co_attainment_view, name='co_attainment'),
    path('co-po-mapping/', views.co_po_mapping_view, name='co_po_mapping'),
]
