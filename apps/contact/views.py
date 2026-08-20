from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ContactForm
from apps.core.models import CompanyInfo


def contact(request):
    company = CompanyInfo.objects.first()

    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Thank you for contacting us! Your message has been received."
            )
            return redirect("contact:contact")
    else:
        form = ContactForm()

    context = {
        "form": form,
        "company": company,
    }
    return render(request, "contact/contact.html", context)