from django.contrib import admin
from .models import Course, Student, Semester

# Register your models here.
class CourseAdmin(admin.ModelAdmin):
     list_display = ('name', 'code')

class StudentAdmin(admin.ModelAdmin):
     list_display = ('first_name', 'last_name')

class SemesterAdmin(admin.ModelAdmin):
     list_display = ('year', 'semester_type')

admin.site.register(Course, CourseAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Semester, SemesterAdmin)
