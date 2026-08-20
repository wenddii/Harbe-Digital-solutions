from django.db import models


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)

    email = models.EmailField()

    phone = models.CharField(
        max_length=20,
        blank=True
    )

    company = models.CharField(
        max_length=100,
        blank=True
    )

    subject = models.CharField(
        max_length=200
    )

    message = models.TextField()

    is_read = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.subject