from django.db import models

# 1. Create the Course Table
class Course(models.Model):
    course_code = models.CharField(max_length=20, unique=True)
    course_name = models.CharField(max_length=100)
    credits = models.IntegerField(default=3)

    def __str__(self):
        return f"{self.course_code} - {self.course_name}"

# 2. Update the Student Table
class Student(models.Model):
    enrollment_number = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    department = models.CharField(max_length=100)
    

    courses = models.ManyToManyField(Course, blank=True, related_name='enrolled_students')
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.enrollment_number})"