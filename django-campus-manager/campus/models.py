from django.db import models

class Student(models.Model):
    enrollment_number = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    department = models.CharField(max_length=100)
    
    # This controls how the object looks in the Django Admin panel
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.enrollment_number})"