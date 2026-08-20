from django.db import models

# Create your models here.
class Project(models.Model):
    title = models.CharField(max_length=200)
    client = models.CharField(max_length=100, blank=True)

    short_description = models.CharField(max_length=255)
    description = models.TextField()

    cover_image = models.ImageField(
        upload_to="projects/",
        blank=True,
        null=True
    )

    project_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)

    is_featured = models.BooleanField(default=False)
    is_completed = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class ProjectImage(models.Model):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="images"
    )

    image = models.ImageField(
        upload_to="projects/gallery/"
    )

    caption = models.CharField(
        max_length=255,
        blank=True
    )

    def __str__(self):
        return f"{self.project.title} Image"