from rest_framework import serializers
from .models import Enrollment, LectureProgress
from courses.serializers import CourseListSerializer


class EnrollmentSerializer(serializers.ModelSerializer):
    course_title = serializers.CharField(source='course.title', read_only=True)
    course_thumbnail = serializers.ImageField(source='course.thumbnail', read_only=True)
    progress_percentage = serializers.FloatField(read_only=True)
    course_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Enrollment
        fields = ['id', 'course_id', 'course_title', 'course_thumbnail', 'enrolled_at', 'status', 'progress_percentage']
        read_only_fields = ['id', 'enrolled_at', 'status']

    def validate_course_id(self, value):
        from courses.models import Course
        try:
            course = Course.objects.get(pk=value, is_published=True)
        except Course.DoesNotExist:
            raise serializers.ValidationError('Course not found or not published.')
        student = self.context['request'].user
        if Enrollment.objects.filter(student=student, course=course).exists():
            raise serializers.ValidationError('You are already enrolled in this course.')
        return value

    def create(self, validated_data):
        from courses.models import Course
        course_id = validated_data.pop('course_id')
        course = Course.objects.get(pk=course_id)
        return Enrollment.objects.create(student=self.context['request'].user, course=course)


class LectureProgressSerializer(serializers.ModelSerializer):
    lecture_title = serializers.CharField(source='lecture.title', read_only=True)

    class Meta:
        model = LectureProgress
        fields = ['id', 'lecture', 'lecture_title', 'completed', 'completed_at']


class ProgressDetailSerializer(serializers.ModelSerializer):
    progress = LectureProgressSerializer(many=True, read_only=True)
    progress_percentage = serializers.FloatField(read_only=True)

    class Meta:
        model = Enrollment
        fields = ['id', 'course', 'progress_percentage', 'status', 'progress']
