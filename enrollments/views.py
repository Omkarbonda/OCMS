from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from accounts.permissions import IsStudent
from .models import Enrollment
from .serializers import EnrollmentSerializer, ProgressDetailSerializer


class EnrollView(generics.CreateAPIView):
    """Student enrolls in a course."""
    permission_classes = [IsStudent]
    serializer_class = EnrollmentSerializer


class MyCoursesView(generics.ListAPIView):
    """List all courses the logged-in student is enrolled in."""
    permission_classes = [IsStudent]
    serializer_class = EnrollmentSerializer

    def get_queryset(self):
        return Enrollment.objects.filter(student=self.request.user).select_related('course')


class CourseProgressView(generics.RetrieveAPIView):
    """Return progress details for a specific enrolled course."""
    permission_classes = [IsStudent]
    serializer_class = ProgressDetailSerializer

    def get_object(self):
        return Enrollment.objects.get(student=self.request.user, course_id=self.kwargs['course_pk'])

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        except Enrollment.DoesNotExist:
            return Response({'error': 'Not enrolled in this course.'}, status=status.HTTP_404_NOT_FOUND)
