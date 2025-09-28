from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Faculty, Department, Subject, Student, Result, FacultySelection, COPO, PredefinedSubject


# Custom User Admin to show Faculty info
class FacultyInline(admin.StackedInline):
    model = Faculty
    can_delete = False
    verbose_name_plural = 'Faculty Profile'


class CustomUserAdmin(UserAdmin):
    inlines = (FacultyInline,)


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = ('user', 'employee_id', 'department', 'designation', 'phone')
    list_filter = ('department', 'designation')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'employee_id')
    ordering = ('user__last_name', 'user__first_name')


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')
    search_fields = ('name', 'code')
    ordering = ('name',)


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'department', 'year', 'scheme', 'credits', 'faculty')
    list_filter = ('department', 'year', 'scheme', 'faculty')
    search_fields = ('name', 'code')
    ordering = ('department', 'year', 'code')


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('roll_number', 'name', 'department', 'year', 'scheme')
    list_filter = ('department', 'year', 'scheme')
    search_fields = ('roll_number', 'name')
    ordering = ('roll_number',)


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ('student', 'subject', 'marks_obtained', 'total_marks', 'status', 'exam_type', 'semester')
    list_filter = ('subject', 'exam_type', 'semester', 'marks_obtained')
    search_fields = ('student__roll_number', 'student__name', 'subject__name')
    ordering = ('-created_at',)


@admin.register(FacultySelection)
class FacultySelectionAdmin(admin.ModelAdmin):
    list_display = ('faculty', 'year', 'scheme', 'department', 'subject')
    list_filter = ('year', 'scheme', 'department')
    search_fields = ('faculty__user__username', 'faculty__user__first_name', 'faculty__user__last_name')
    ordering = ('-created_at',)


@admin.register(COPO)
class COPOAdmin(admin.ModelAdmin):
    list_display = ('subject', 'co_number', 'co_description')
    list_filter = ('subject',)
    search_fields = ('subject__name', 'co_number', 'co_description')
    ordering = ('subject', 'co_number')


@admin.register(PredefinedSubject)
class PredefinedSubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'department', 'active', 'created_at')
    list_filter = ('department', 'active')
    search_fields = ('name', 'department__name')
    ordering = ('department', 'name')


# Customize admin site
admin.site.site_header = "Faculty Portal Administration"
admin.site.site_title = "Faculty Portal Admin"
admin.site.index_title = "Welcome to Faculty Portal Administration"