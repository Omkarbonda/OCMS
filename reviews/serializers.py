from rest_framework import serializers
from .models import Review


class ReviewSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.full_name', read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'student_name', 'course', 'rating', 'comment', 'created_at']
        read_only_fields = ['id', 'student_name', 'created_at']

    def validate(self, data):
        request = self.context.get('request')
        course = data.get('course') or self.instance.course if self.instance else None
        if course and Review.objects.filter(student=request.user, course=course).exists():
            if not self.instance:  # creating, not updating
                raise serializers.ValidationError('You have already reviewed this course.')
        return data

    def create(self, validated_data):
        validated_data['student'] = self.context['request'].user
        return super().create(validated_data)
