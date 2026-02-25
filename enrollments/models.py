from django.db import models
from django.conf import settings
from courses.models import Course, Lecture


class Enrollment(models.Model):
    STATUS_CHOICES = (
        ('ACTIVE', 'Active'),
        ('COMPLETED', 'Completed'),
    )

    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='enrollments',
        limit_choices_to={'role': 'STUDENT'},
    )
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIVE', db_index=True)
    enrolled_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'course')
        ordering = ['-enrolled_at']

    def __str__(self):
        return f"{self.student.email} → {self.course.title}"

    @property
    def progress_percentage(self):
        total = self.course.modules.aggregate(
            total=models.Count('lectures')
        )['total'] or 0
        if total == 0:
            return 0
        completed = self.progress.filter(completed=True).count()
        return round((completed / total) * 100, 1)


class LectureProgress(models.Model):
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE, related_name='progress')
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True, db_index=True)

    class Meta:
        unique_together = ('enrollment', 'lecture')

    def __str__(self):
        return f"{self.enrollment} – {self.lecture.title} ({'done' if self.completed else 'pending'})"
