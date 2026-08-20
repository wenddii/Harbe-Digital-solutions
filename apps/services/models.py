from django.db import models


class Service(models.Model):
    name = models.CharField(max_length=100)
    short_description = models.CharField(max_length=200)
    description = models.TextField()

    icon = models.CharField(
        max_length=100,
        help_text="Example: fa-solid fa-code"
    )

    image = models.ImageField(
        upload_to="services/",
        blank=True,
        null=True
    )

    is_featured = models.BooleanField(default=False)

    def __str__(self):
        return self.name