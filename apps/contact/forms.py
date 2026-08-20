from django import forms
from .models import ContactMessage


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ["name", "email", "phone", "company", "subject", "message"]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Your Name"}),
            "email": forms.EmailInput(attrs={"placeholder": "Your Email Address"}),
            "phone": forms.TextInput(attrs={"placeholder": "Your Phone Number (optional)"}),
            "company": forms.TextInput(attrs={"placeholder": "Company Name (optional)"}),
            "subject": forms.TextInput(attrs={"placeholder": "Subject"}),
            "message": forms.Textarea(attrs={"rows": 5, "placeholder": "Write your message here..."}),
        }
