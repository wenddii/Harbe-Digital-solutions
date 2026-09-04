from django.shortcuts import render
from .models import CompanyInfo, FAQ
from apps.services.models import Service
from apps.portfolio.models import Project


def home(request):
    company = CompanyInfo.objects.first()
    featured_services = Service.objects.filter(is_featured=True)
    featured_projects = Project.objects.filter(is_featured=True)
    faqs = FAQ.objects.all()

    context = {
        "company": company,
        "featured_services": featured_services,
        "featured_projects": featured_projects,
        "faqs": faqs,
    }
    return render(request, "core/home.html", context)


def about(request):
    company = CompanyInfo.objects.first()

    context = {
        "company": company,
    }
    return render(request, "core/about.html", context)