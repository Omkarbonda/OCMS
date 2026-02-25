from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny

from accounts.permissions import IsStudent
from .models import Review
from .serializers import ReviewSerializer


class CourseReviewListCreateView(generics.ListCreateAPIView):
    serializer_class = ReviewSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsStudent()]

    def get_queryset(self):
        return Review.objects.filter(course_id=self.kwargs['course_pk']).select_related('student')

    def perform_create(self, serializer):
        from courses.models import Course
        course = Course.objects.get(pk=self.kwargs['course_pk'])
        serializer.save(student=self.request.user, course=course)


class MyReviewsView(generics.ListAPIView):
    permission_classes = [IsStudent]
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(student=self.request.user).select_related('course')
