from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def subjectspage_view(request):
    return render(request, 'dashboard/subjectspage.html')
