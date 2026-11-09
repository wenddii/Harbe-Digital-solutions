from django.urls import path
from . import views

app_name = "services"

urlpatterns = [
    path("<int:pk>/", views.service_detail, name="detail"),
]