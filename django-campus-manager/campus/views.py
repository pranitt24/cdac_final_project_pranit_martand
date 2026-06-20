from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Student

# This simple tag acts as a bouncer for this specific page
@login_required
def student_directory(request):
    all_students = Student.objects.all()
    context = {'students': all_students}
    return render(request, 'campus/student_directory.html', context)

def student_directory(request):
    # Fetch all students from the database
    all_students = Student.objects.all()
    
    # Pass them to an HTML file (which we will create next)
    context = {'students': all_students}
    return render(request, 'campus/student_directory.html', context)