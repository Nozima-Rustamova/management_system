from django.contrib import admin
from . import models

@admin.register(models.Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('user', 'subject')

@admin.register(models.Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'teacher', 'schedule')

@admin.register(models.Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'join_date')
    filter_horizontal = ('enrolled_groups',)
