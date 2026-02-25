from django.urls import path
from .views import (
    CategoryListCreateView, CategoryDetailView,
    CourseListView, CourseDetailView,
    InstructorCourseListCreateView, InstructorCourseDetailView,
    ModuleListCreateView, LectureListCreateView,
)

urlpatterns = [
    # Categories
    path('categories/', CategoryListCreateView.as_view(), name='category-list'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),

    # Public course endpoints
    path('courses/', CourseListView.as_view(), name='course-list'),
    path('courses/<int:pk>/', CourseDetailView.as_view(), name='course-detail'),

    # Instructor endpoints
    path('instructor/courses/', InstructorCourseListCreateView.as_view(), name='instructor-courses'),
    path('instructor/courses/<int:pk>/', InstructorCourseDetailView.as_view(), name='instructor-course-detail'),
    path('instructor/courses/<int:course_pk>/modules/', ModuleListCreateView.as_view(), name='module-list'),
    path('instructor/courses/<int:course_pk>/modules/<int:module_pk>/lectures/', LectureListCreateView.as_view(), name='lecture-list'),
]
