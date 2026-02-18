from django.urls import path

from .views import (
    # auth
    CustomLoginView,
    CustomLogoutView,
    register_view,
    RedirectAfterLoginView,

    # dashboards
    StudentListView,
    StudentDashboardView,

    # student features
    StudentCreateView,
    AttendanceUpdateView,
    MarksUpdateView,
    StudentReportView,
)

urlpatterns = [

    # =====================
    # AUTHENTICATION
    # =====================
    path('accounts/login/', CustomLoginView.as_view(), name='login'),
    path('accounts/logout/', CustomLogoutView.as_view(), name='logout'),
    path('register/', register_view, name='register'),
    path('redirect-after-login/', RedirectAfterLoginView.as_view(), name='redirect_after_login'),

    # =====================
    # DASHBOARDS
    # =====================
    path('', StudentListView.as_view(), name='student_list'),              # Teacher/Admin
    path('student/dashboard/', StudentDashboardView.as_view(), name='student_dashboard'),

    # =====================
    # STUDENT MANAGEMENT (Teacher only)
    # =====================
    path('add/', StudentCreateView.as_view(), name='add_student'),
    path('attendance/<int:pk>/', AttendanceUpdateView.as_view(), name='mark_attendance'),
    path('marks/<int:pk>/', MarksUpdateView.as_view(), name='enter_marks'),
    path('report/<int:pk>/', StudentReportView.as_view(), name='student_report'),
]