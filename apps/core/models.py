from django.db import models


class CompanyInfo(models.Model):
    name = models.CharField(max_length=100)
    tagline = models.CharField(max_length=200)
    about = models.TextField()

    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=255)

    logo = models.ImageField(upload_to="company/", blank=True, null=True)

    facebook = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    github = models.URLField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name



class TeamMember(models.Model):
    full_name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    bio = models.TextField()

    photo = models.ImageField(upload_to="team/", blank=True, null=True)

    email = models.EmailField(blank=True)
    linkedin = models.URLField(blank=True)
    github = models.URLField(blank=True)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.full_name


class FAQ(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()

    def __str__(self):
        return self.question