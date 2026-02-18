"""
admin.py
========
Django Admin Configuration for
AI-Assisted Smart Attendance & Performance Tracker
"""

from django.contrib import admin
from .models import Student, AttendanceRecord, Mark


# -------------------------------------------------
# STUDENT ADMIN
# -------------------------------------------------
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):

    list_display = (
        'roll_no',
        'name',
        'semester',
        'attendance_percentage',
        'attendance_shortage'
    )

    list_display_links = ('roll_no', 'name')
    list_filter = ('semester',)
    search_fields = ('roll_no', 'name')
    ordering = ('roll_no',)

    # Custom column: Attendance %
    def attendance_percentage(self, obj):
        return f"{obj.get_attendance_percentage()}%"
    attendance_percentage.short_description = "Attendance %"

    # Custom column: Attendance Warning
    def attendance_shortage(self, obj):
        return "⚠ Shortage" if obj.has_attendance_shortage() else "OK"
    attendance_shortage.short_description = "Attendance Status"


# -------------------------------------------------
# ATTENDANCE RECORD ADMIN
# -------------------------------------------------
@admin.register(AttendanceRecord)
class AttendanceRecordAdmin(admin.ModelAdmin):

    list_display = (
        'student',
        'date',
        'total_lectures',
        'attended_lectures',
        'percentage'
    )

    list_filter = ('date',)
    search_fields = ('student__name', 'student__roll_no')
    ordering = ('-date',)

    def percentage(self, obj):
        total = obj.total_lectures
        if total == 0:
            return "0%"
        return f"{round((obj.attended_lectures / total) * 100, 2)}%"
    percentage.short_description = "Attendance %"


# -------------------------------------------------
# MARK / PERFORMANCE ADMIN
# -------------------------------------------------
@admin.register(Mark)
class MarkAdmin(admin.ModelAdmin):

    list_display = (
        'student',
        'marks_obtained',
        'performance_remark'
    )

    search_fields = ('student__name', 'student__roll_no')

    def performance_remark(self, obj):
        return obj.get_performance_remark()
    performance_remark.short_description = "AI Performance Remark"