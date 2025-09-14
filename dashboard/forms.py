
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Department, Subject


class FacultyLoginForm(AuthenticationForm):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
            'placeholder': 'Enter your username'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
            'placeholder': 'Enter your password'
        })
    )


class FacultySelectionForm(forms.Form):
    YEAR_CHOICES = [
        (1, '1st Year'),
        (2, '2nd Year'),
        (3, '3rd Year'),
        (4, '4th Year'),
    ]
    
    SCHEME_CHOICES = [
        ('R19-20', 'R19-20'),
        ('NEP', 'NEP'),
        ('AUTONOMOUS', 'Autonomous'),
    ]
    
    year = forms.ChoiceField(
        choices=YEAR_CHOICES,
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent'
        })
    )
    
    scheme = forms.ChoiceField(
        choices=SCHEME_CHOICES,
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent'
        })
    )
    
    department = forms.ModelChoiceField(
        queryset=Department.objects.all(),
        empty_label="Select Department",
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent'
        })
    )
    
    subject = forms.ModelChoiceField(
        queryset=Subject.objects.none(),
        required=False,
        empty_label="Select Subject (Optional)",
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent'
        })
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'department' in self.data:
            try:
                department_id = int(self.data.get('department'))
                self.fields['subject'].queryset = Subject.objects.filter(department_id=department_id)
            except (ValueError, TypeError):
                pass
        elif hasattr(self, 'instance') and self.instance and hasattr(self.instance, 'pk') and self.instance.pk:
            self.fields['subject'].queryset = self.instance.department.subject_set
