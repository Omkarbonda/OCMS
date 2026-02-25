from django.urls import path
from .views import AnalyticsView, TopCoursesView

urlpatterns = [
    path('analytics/', AnalyticsView.as_view(), name='admin-analytics'),
    path('top-courses/', TopCoursesView.as_view(), name='admin-top-courses'),
]
