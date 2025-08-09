from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, 'sales/home.html')

@login_required
def records(request):
    return render(request, 'sales/records.html')
