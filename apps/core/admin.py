from django.contrib import admin
from .models import CompanyInfo, TeamMember, FAQ

admin.site.register(CompanyInfo)
admin.site.register(TeamMember)
admin.site.register(FAQ)