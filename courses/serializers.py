from rest_framework import serializers
from .models import Category, Course, Module, Lecture


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description']


class LectureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lecture
        fields = ['id', 'title', 'notes', 'video_url', 'order', 'is_free', 'duration']


class ModuleSerializer(serializers.ModelSerializer):
    lectures = LectureSerializer(many=True, read_only=True)

    class Meta:
        model = Module
        fields = ['id', 'title', 'order', 'lectures']


class CourseListSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source='category', write_only=True, required=False
    )
    instructor_name = serializers.CharField(source='instructor.full_name', read_only=True)
    enrollment_count = serializers.IntegerField(read_only=True)
    average_rating = serializers.FloatField(read_only=True)

    class Meta:
        model = Course
        fields = [
            'id', 'title', 'description', 'instructor_name', 'category', 'category_id',
            'price', 'level', 'thumbnail', 'is_published', 'enrollment_count',
            'average_rating', 'created_at',
        ]


class CourseDetailSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    modules = ModuleSerializer(many=True, read_only=True)
    instructor_name = serializers.CharField(source='instructor.full_name', read_only=True)
    instructor_bio = serializers.CharField(source='instructor.bio', read_only=True)
    enrollment_count = serializers.IntegerField(read_only=True)
    average_rating = serializers.FloatField(read_only=True)

    class Meta:
        model = Course
        fields = [
            'id', 'title', 'description', 'instructor_name', 'instructor_bio',
            'category', 'price', 'level', 'thumbnail', 'is_published',
            'modules', 'enrollment_count', 'average_rating', 'created_at', 'updated_at',
        ]


class CourseCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'category', 'price', 'level', 'thumbnail', 'is_published']

    def create(self, validated_data):
        validated_data['instructor'] = self.context['request'].user
        return super().create(validated_data)
