from django.shortcuts import render
from .models import CompanyInfo, TeamMember, FAQ
from apps.services.models import Service
from apps.portfolio.models import Project


def home(request):
    company = CompanyInfo.objects.first()
    featured_services = Service.objects.filter(is_featured=True)
    featured_projects = Project.objects.filter(is_featured=True)
    team_members = TeamMember.objects.filter(is_active=True)
    faqs = FAQ.objects.all()

    context = {
        "company": company,
        "featured_services": featured_services,
        "featured_projects": featured_projects,
        "team_members": team_members,
        "faqs": faqs,
    }
    return render(request, "core/home.html", context)


def about(request):
    company = CompanyInfo.objects.first()
    team_members = TeamMember.objects.filter(is_active=True)

    context = {
        "company": company,
        "team_members": team_members,
    }
    return render(request, "core/about.html", context)