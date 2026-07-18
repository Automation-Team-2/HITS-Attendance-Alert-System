from django.contrib import admin
from .models import Section, Student


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('roll', 'name', 'section', 'contact', 'attendance')
    list_filter = ('section',)
    search_fields = ('roll', 'name')
