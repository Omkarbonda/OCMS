from django.core.cache import cache
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from accounts.permissions import IsAdmin
from accounts.models import User
from courses.models import Course
from enrollments.models import Enrollment


# Detailed Schema Redis Keys
CACHE_KEYS = {
    'USERS_COUNT': 'admin:users:count',
    'COURSES_COUNT': 'admin:courses:count',
    'TOP_COURSES': 'admin:top:courses',
    'ENROLLMENTS_COUNT': 'admin:enrollments:count',
}
CACHE_TTL = 60 * 15  # 15 minutes as per design note


class AnalyticsView(APIView):
    """Platform-wide statistics for admin users using Redis caching."""
    permission_classes = [IsAdmin]

    def get(self, request):
        # Users Count
        total_students = cache.get(CACHE_KEYS['USERS_COUNT'])
        if total_students is None:
            total_students = User.objects.filter(role='STUDENT').count()
            cache.set(CACHE_KEYS['USERS_COUNT'], total_students, CACHE_TTL)

        # Courses Count
        total_courses = cache.get(CACHE_KEYS['COURSES_COUNT'])
        if total_courses is None:
            total_courses = Course.objects.count()
            cache.set(CACHE_KEYS['COURSES_COUNT'], total_courses, CACHE_TTL)

        # Enrollments Count
        total_enrollments = cache.get(CACHE_KEYS['ENROLLMENTS_COUNT'])
        if total_enrollments is None:
            total_enrollments = Enrollment.objects.count()
            cache.set(CACHE_KEYS['ENROLLMENTS_COUNT'], total_enrollments, CACHE_TTL)

        data = {
            'total_students': total_students,
            'total_instructors': User.objects.filter(role='INSTRUCTOR').count(),
            'total_courses': total_courses,
            'published_courses': Course.objects.filter(is_published=True).count(),
            'total_enrollments': total_enrollments,
            'completed_enrollments': Enrollment.objects.filter(status='COMPLETED').count(),
        }
        return Response(data)


class TopCoursesView(APIView):
    """Top 5 courses by enrollment count – Redis cached."""
    permission_classes = [IsAdmin]

    def get(self, request):
        cached = cache.get(CACHE_KEYS['TOP_COURSES'])
        if cached:
            return Response(cached)

        from django.db.models import Count
        top = (
            Course.objects.filter(is_published=True)
            .annotate(enrollment_count=Count('enrollments'))
            .order_by('-enrollment_count')[:5]
            .values('id', 'title', 'level', 'price', 'enrollment_count')
        )
        result = list(top)
        cache.set(CACHE_KEYS['TOP_COURSES'], result, CACHE_TTL)
        return Response(result)
