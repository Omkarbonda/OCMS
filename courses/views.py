from django.core.cache import cache
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from accounts.permissions import IsInstructor, IsAdmin
from .models import Category, Course, Module, Lecture
from .serializers import (
    CategorySerializer, CourseListSerializer, CourseDetailSerializer,
    CourseCreateUpdateSerializer, ModuleSerializer, LectureSerializer
)
from .filters import CourseFilter


COURSE_LIST_CACHE_KEY = 'public_course_list'
CACHE_TTL = 60 * 5  # 5 minutes


class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    search_fields = ['name']


class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdmin]


class CourseListView(generics.ListAPIView):
    """Public course listing with Redis caching, filtering, searching, and ordering."""
    serializer_class = CourseListSerializer
    permission_classes = [AllowAny]
    filterset_class = CourseFilter
    search_fields = ['title', 'description', 'instructor__full_name']
    ordering_fields = ['price', 'created_at', 'enrollment_count']
    ordering = ['-created_at']

    def get_queryset(self):
        return Course.objects.filter(is_published=True).select_related('category', 'instructor')

    def list(self, request, *args, **kwargs):
        # Only cache unfiltered requests
        if not request.query_params:
            cached = cache.get(COURSE_LIST_CACHE_KEY)
            if cached:
                return Response(cached)

        response = super().list(request, *args, **kwargs)

        if not request.query_params:
            cache.set(COURSE_LIST_CACHE_KEY, response.data, CACHE_TTL)

        return response


class CourseDetailView(generics.RetrieveAPIView):
    queryset = Course.objects.filter(is_published=True).select_related('category', 'instructor').prefetch_related('modules__lectures')
    serializer_class = CourseDetailSerializer
    permission_classes = [AllowAny]


class InstructorCourseListCreateView(generics.ListCreateAPIView):
    """Instructor creates and lists their own courses."""
    permission_classes = [IsInstructor]
    serializer_class = CourseCreateUpdateSerializer

    def get_queryset(self):
        return Course.objects.filter(instructor=self.request.user)

    def perform_create(self, serializer):
        cache.delete(COURSE_LIST_CACHE_KEY)
        serializer.save(instructor=self.request.user)


class InstructorCourseDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Instructor manages a specific course they own."""
    permission_classes = [IsInstructor]
    serializer_class = CourseCreateUpdateSerializer

    def get_queryset(self):
        return Course.objects.filter(instructor=self.request.user)

    def perform_update(self, serializer):
        cache.delete(COURSE_LIST_CACHE_KEY)
        serializer.save()

    def perform_destroy(self, instance):
        cache.delete(COURSE_LIST_CACHE_KEY)
        instance.delete()


class ModuleListCreateView(generics.ListCreateAPIView):
    serializer_class = ModuleSerializer
    permission_classes = [IsInstructor]

    def get_queryset(self):
        return Module.objects.filter(course__instructor=self.request.user, course_id=self.kwargs['course_pk'])

    def perform_create(self, serializer):
        course = Course.objects.get(pk=self.kwargs['course_pk'], instructor=self.request.user)
        serializer.save(course=course)


class LectureListCreateView(generics.ListCreateAPIView):
    serializer_class = LectureSerializer
    permission_classes = [IsInstructor]

    def get_queryset(self):
        return Lecture.objects.filter(
            module_id=self.kwargs['module_pk'],
            module__course__instructor=self.request.user
        )

    def perform_create(self, serializer):
        module = Module.objects.get(pk=self.kwargs['module_pk'], course__instructor=self.request.user)
        serializer.save(module=module)
