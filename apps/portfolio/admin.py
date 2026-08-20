from django.contrib import admin
from .models import Project, ProjectImage


class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "client", "is_featured", "is_completed", "created_at")
    list_filter = ("is_featured", "is_completed", "created_at")
    search_fields = ("title", "client", "description")
    inlines = [ProjectImageInline]


@admin.register(ProjectImage)
class ProjectImageAdmin(admin.ModelAdmin):
    list_display = ("project", "caption")
    search_fields = ("project__title", "caption")