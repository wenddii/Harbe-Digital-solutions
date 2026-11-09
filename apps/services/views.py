from django.shortcuts import get_object_or_404, render

from .models import Service


def service_detail(request, pk):
    service = get_object_or_404(Service, pk=pk)

    return render(
        request,
        "services/detail.html",
        {"service": service}
    )