# from django import forms
# from .models import Student, AttendanceRecord, Mark


# # -------------------------------------------------
# # 1. STUDENT FORM (Add New Student)
# # -------------------------------------------------
# class StudentForm(forms.ModelForm):
#     class Meta:
#         model = Student
#         fields = ['roll_no', 'name', 'semester']

#         widgets = {
#             'roll_no': forms.NumberInput(attrs={
#                 'class': 'form-control',
#                 'placeholder': 'e.g. 101'
#             }),
#             'name': forms.TextInput(attrs={
#                 'class': 'form-control',
#                 'placeholder': 'Full Name'
#             }),
#             'semester': forms.NumberInput(attrs={
#                 'class': 'form-control',
#                 'placeholder': '1 to 8'
#             }),
#         }


# # -------------------------------------------------
# # 2. ATTENDANCE FORM
# # -------------------------------------------------
# class AttendanceForm(forms.ModelForm):
#     class Meta:
#         model = AttendanceRecord
#         fields = ['student', 'total_lectures', 'attended_lectures']

#         widgets = {
#             'student': forms.Select(attrs={'class': 'form-control'}),
#             'total_lectures': forms.NumberInput(attrs={'class': 'form-control'}),
#             'attended_lectures': forms.NumberInput(attrs={'class': 'form-control'}),
#         }

#     # Validation: Attended <= Total
#     def clean(self):
#         cleaned_data = super().clean()
#         total = cleaned_data.get('total_lectures')
#         attended = cleaned_data.get('attended_lectures')

#         if total is not None and attended is not None:
#             if attended > total:
#                 raise forms.ValidationError(
#                     "Attended lectures cannot be greater than total lectures."
#                 )
#         return cleaned_data


# # -------------------------------------------------
# # 3. MARKS FORM
# # -------------------------------------------------
# class MarksForm(forms.ModelForm):
#     class Meta:
#         model = Mark
#         fields = ['student', 'marks_obtained']

#         widgets = {
#             'student': forms.Select(attrs={'class': 'form-control'}),
#             'marks_obtained': forms.NumberInput(attrs={
#                 'class': 'form-control',
#                 'placeholder': 'Enter marks (0-100)'
#             }),
#         }

#     # Validation: 0–100
#     def clean_marks_obtained(self):
#         marks = self.cleaned_data.get('marks_obtained')
#         if marks < 0 or marks > 100:
#             raise forms.ValidationError(
#                 "Marks must be between 0 and 100."
#             )
#         return marks



from django import forms
from .models import Student, AttendanceRecord, Mark


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['roll_no', 'name', 'semester']
        widgets = {
            'roll_no': forms.NumberInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'semester': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class AttendanceForm(forms.ModelForm):
    class Meta:
        model = AttendanceRecord
        fields = ['total_lectures', 'attended_lectures']
        widgets = {
            'total_lectures': forms.NumberInput(attrs={'class': 'form-control'}),
            'attended_lectures': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class MarksForm(forms.ModelForm):
    class Meta:
        model = Mark
        fields = ['marks_obtained']
        widgets = {
            'marks_obtained': forms.NumberInput(attrs={'class': 'form-control'}),
        }