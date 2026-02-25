from django.urls import path
from .views import EnrollView, MyCoursesView, CourseProgressView

urlpatterns = [
    path('enroll/', EnrollView.as_view(), name='enroll'),
    path('my-courses/', MyCoursesView.as_view(), name='my-courses'),
    path('course/<int:course_pk>/progress/', CourseProgressView.as_view(), name='course-progress'),
]
