"""Frontend page URL routes served by Django for HTML templates."""

from django.urls import path
from django.views.generic import TemplateView

urlpatterns = [
    path('', TemplateView.as_view(template_name='course_list.html'), name='home'),
    path('login/', TemplateView.as_view(template_name='login.html'), name='login-page'),
    path('register/', TemplateView.as_view(template_name='register.html'), name='register-page'),
    path('student/dashboard/', TemplateView.as_view(template_name='student_dashboard.html'), name='student-dashboard'),
    path('courses/<int:pk>/', TemplateView.as_view(template_name='course_detail.html'), name='course-detail-page'),
    path('instructor/dashboard/', TemplateView.as_view(template_name='instructor_dashboard.html'), name='instructor-dashboard'),
    path('admin-dashboard/', TemplateView.as_view(template_name='admin_dashboard.html'), name='admin-dashboard-page'),
]
