from django.contrib import admin
from .models import Category, Course, Module, Lecture


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


class ModuleInline(admin.TabularInline):
    model = Module
    extra = 0


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'instructor', 'category', 'level', 'price', 'is_published', 'enrollment_count')
    list_filter = ('level', 'is_published', 'category')
    search_fields = ('title', 'instructor__email')
    inlines = [ModuleInline]


class LectureInline(admin.TabularInline):
    model = Lecture
    extra = 0


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'order')
    inlines = [LectureInline]


@admin.register(Lecture)
class LectureAdmin(admin.ModelAdmin):
    list_display = ('title', 'module', 'order', 'is_free', 'duration')
