from django.views.generic import ListView, CreateView, DetailView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.models import User
from .models import Student, AttendanceRecord, Mark
from .forms import StudentForm, AttendanceForm, MarksForm


# -------------------------------------------------
# CUSTOM LOGOUT VIEW (supports GET and POST)
# -------------------------------------------------
class CustomLogoutView(LogoutView):
    """Custom logout that accepts both GET and POST for convenience"""
    def get(self, request, *args, **kwargs):
        # Allow GET requests by converting to POST
        return super().post(request, *args, **kwargs)


# -------------------------------------------------
# LOGIN VIEW (with validation message)
# -------------------------------------------------
class CustomLoginView(LoginView):
    template_name = 'registration/login.html'

    def form_invalid(self, form):
        messages.error(
            self.request,
            "Invalid username or password. Please try again."
        )
        return super().form_invalid(form)


# -------------------------------------------------
# REGISTER VIEW (New User Creation)
# -------------------------------------------------
def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if not username or not password1 or not password2:
            messages.error(request, "All fields are required")
            return redirect("register")

        if password1 != password2:
            messages.error(request, "Passwords do not match")
            return redirect("register")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect("register")

        User.objects.create_user(
            username=username,
            password=password1
        )

        messages.success(request, "Account created successfully. Please login.")
        return redirect("login")

    return render(request, "registration/register.html")


# -------------------------------------------------
# STUDENT LIST / DASHBOARD
# -------------------------------------------------
class StudentListView(LoginRequiredMixin, ListView):
    model = Student
    template_name = 'tracker/student_list.html'
    context_object_name = 'students'
    login_url = 'login'


# -------------------------------------------------
# ADD STUDENT
# -------------------------------------------------
class StudentCreateView(LoginRequiredMixin, CreateView):
    model = Student
    form_class = StudentForm
    template_name = "tracker/student_form.html"
    success_url = reverse_lazy('student_list')
    login_url = 'login'


# -------------------------------------------------
# MARK ATTENDANCE
# -------------------------------------------------
class AttendanceUpdateView(LoginRequiredMixin, CreateView):
    model = AttendanceRecord
    form_class = AttendanceForm
    template_name = "tracker/attendance_form.html"
    login_url = 'login'

    def form_valid(self, form):
        form.instance.student = Student.objects.get(pk=self.kwargs['pk'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('student_list')


# -------------------------------------------------
# ENTER MARKS
# -------------------------------------------------
class MarksUpdateView(LoginRequiredMixin, CreateView):
    model = Mark
    form_class = MarksForm
    template_name = "tracker/marks_form.html"
    login_url = 'login'

    def form_valid(self, form):
        form.instance.student = Student.objects.get(pk=self.kwargs['pk'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('student_list')


# -------------------------------------------------
# STUDENT REPORT
# -------------------------------------------------


class StudentReportView(LoginRequiredMixin, DetailView):
    model = Student
    template_name = 'tracker/student_report.html'
    context_object_name = 'student'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        student = self.get_object()
        attendance_records = AttendanceRecord.objects.filter(student=student)

        total_lectures = 0
        attended_lectures = 0

        for record in attendance_records:
            total_lectures += record.total_lectures
            attended_lectures += record.attended_lectures

        attendance_percentage = (
            (attended_lectures / total_lectures) * 100
            if total_lectures > 0 else 0
        )

        mark = Mark.objects.filter(student=student).first()

        context.update({
            'attendance_records': attendance_records,
            'total_lectures': total_lectures,
            'attended_lectures': attended_lectures,
            'attendance_percentage': round(attendance_percentage, 2),
            'mark': mark,
        })

        return context
    
    
    
from django.contrib.auth.forms import UserCreationForm
from django.views import View
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Student

from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .models import Student

class StudentRegisterView(View):
    def get(self, request):
        form = UserCreationForm()
        return render(request, 'registration/register.html', {'form': form})

    def post(self, request):
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()

            # 🔗 LINK USER WITH STUDENT
            Student.objects.create(
                user=user,
                roll_no=user.id + 1000,   # simple auto roll
                name=user.username,
                semester=1
            )

            messages.success(request, "Account created successfully. Please login.")
            return redirect('login')

        return render(request, 'registration/register.html', {'form': form})
    
    
    
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from .models import Student, Mark

class StudentDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'student/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        student = Student.objects.get(user=self.request.user)
        mark = Mark.objects.filter(student=student).first()

        context['student'] = student
        context['mark'] = mark

        return context
    
    
    
    
from django.shortcuts import redirect
from django.views import View
from django.contrib.auth.models import User
from .models import Student

class RedirectAfterLoginView(View):
    def get(self, request):
        user = request.user

        # 👑 Superuser / Teacher
        if user.is_superuser or user.is_staff:
            return redirect('student_list')

        # 🎓 Student
        try:
            Student.objects.get(user=user)
            return redirect('student_dashboard')
        except Student.DoesNotExist:
            return redirect('login')