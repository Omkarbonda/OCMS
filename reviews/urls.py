from django.urls import path
from .views import CourseReviewListCreateView, MyReviewsView

urlpatterns = [
    path('courses/<int:course_pk>/reviews/', CourseReviewListCreateView.as_view(), name='course-reviews'),
    path('reviews/my/', MyReviewsView.as_view(), name='my-reviews'),
]
