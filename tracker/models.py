# from django.db import models
# from django.core.validators import MinValueValidator, MaxValueValidator
# from django.utils import timezone


# # -------------------------------------------------
# # STUDENT MODEL
# # -------------------------------------------------
# class Student(models.Model):
#     """
#     Student Model
#     Stores basic student details
#     """
#     roll_no = models.IntegerField(
#         unique=True,
#         validators=[MinValueValidator(1), MaxValueValidator(9999)],
#         help_text="Unique Roll Number (1-9999)"
#     )
#     name = models.CharField(max_length=100)
#     semester = models.IntegerField(
#         validators=[MinValueValidator(1), MaxValueValidator(8)],
#         help_text="Semester (1-8)"
#     )

#     def __str__(self):
#         return f"{self.roll_no} - {self.name}"

#     # -------------------------------
#     # AI-ASSISTED ATTENDANCE LOGIC
#     # -------------------------------
#     def get_total_lectures(self):
#         latest = self.attendance_records.order_by('-date').first()
#         return latest.total_lectures if latest else 0

#     def get_attended_lectures(self):
#         latest = self.attendance_records.order_by('-date').first()
#         return latest.attended_lectures if latest else 0

#     def get_attendance_percentage(self):
#         total = self.get_total_lectures()
#         if total == 0:
#             return 0.0
#         attended = self.get_attended_lectures()
#         return round((attended / total) * 100, 2)

#     def has_attendance_shortage(self):
#         """AI Logic: Attendance below 75%"""
#         return self.get_attendance_percentage() < 75


# # -------------------------------------------------
# # ATTENDANCE RECORD MODEL
# # -------------------------------------------------
# class AttendanceRecord(models.Model):
#     """
#     Stores attendance details of a student
#     """
#     student = models.ForeignKey(
#         Student,
#         on_delete=models.CASCADE,
#         related_name='attendance_records'
#     )
#     date = models.DateTimeField(default=timezone.now)
#     total_lectures = models.IntegerField(
#         validators=[MinValueValidator(1)]
#     )
#     attended_lectures = models.IntegerField(
#         validators=[MinValueValidator(0)]
#     )

#     class Meta:
#         ordering = ['-date']

#     def __str__(self):
#         return f"{self.student.name} - {self.date.date()}"

#     def clean(self):
#         from django.core.exceptions import ValidationError
#         if self.attended_lectures > self.total_lectures:
#             raise ValidationError("Attended lectures cannot exceed total lectures")

#     def save(self, *args, **kwargs):
#         self.clean()
#         super().save(*args, **kwargs)


# # -------------------------------------------------
# # MARK / PERFORMANCE MODEL (ONE SUBJECT)
# # -------------------------------------------------
# class Mark(models.Model):
#     """
#     Stores marks for one subject (as per problem statement)
#     """
#     student = models.OneToOneField(
#         Student,
#         on_delete=models.CASCADE,
#         related_name='mark'
#     )
#     marks_obtained = models.IntegerField(
#         validators=[MinValueValidator(0), MaxValueValidator(100)],
#         help_text="Marks out of 100"
#     )

#     def __str__(self):
#         return f"{self.student.name} - {self.marks_obtained}"

#     # -------------------------------
#     # AI-ASSISTED PERFORMANCE LOGIC
#     # -------------------------------
#     def get_performance_remark(self):
#         """
#         AI Generated Performance Remark
#         """
#         if self.marks_obtained >= 75:
#             return "Good"
#         elif self.marks_obtained >= 50:
#             return "Average"
#         else:
#             return "Needs Improvement"




from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone


from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User

class Student(models.Model):
    # 🔑 NEW (for login linking)
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    roll_no = models.IntegerField(unique=True)
    name = models.CharField(max_length=100)
    semester = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(8)]
    )

    def __str__(self):
        return f"{self.roll_no} - {self.name}"

    # -------- Attendance helpers (UNCHANGED) --------
    def get_total_lectures(self):
        latest = self.attendance_records.first()
        return latest.total_lectures if latest else 0

    def get_attended_lectures(self):
        latest = self.attendance_records.first()
        return latest.attended_lectures if latest else 0

    def get_attendance_percentage(self):
        total = self.get_total_lectures()
        if total == 0:
            return 0
        return round((self.get_attended_lectures() / total) * 100, 2)

    def has_attendance_shortage(self):
        return self.get_attendance_percentage() < 75

class AttendanceRecord(models.Model):
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="attendance_records"
    )
    date = models.DateTimeField(default=timezone.now)
    total_lectures = models.IntegerField(validators=[MinValueValidator(1)])
    attended_lectures = models.IntegerField(validators=[MinValueValidator(0)])

    class Meta:
        ordering = ['-date']

    def clean(self):
        if self.attended_lectures > self.total_lectures:
            raise ValueError("Attended lectures cannot exceed total lectures")

    def __str__(self):
        return f"{self.student.name} attendance"


class Mark(models.Model):
    student = models.OneToOneField(
        Student,
        on_delete=models.CASCADE,
        related_name="mark"
    )
    marks_obtained = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])

    def get_performance_remark(self):
        if self.marks_obtained >= 75:
            return "Good"
        elif self.marks_obtained >= 50:
            return "Average"
        return "Needs Improvement"

    def __str__(self):
        return f"{self.student.name} marks"