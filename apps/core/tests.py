from django.test import TestCase, Client
from django.urls import reverse
from apps.core.models import CompanyInfo, TeamMember, FAQ
from apps.services.models import Service
from apps.portfolio.models import Project, ProjectImage
from apps.contact.models import ContactMessage


class WebsiteTests(TestCase):
    def setUp(self):
        self.client = Client()

        # Company info
        self.company = CompanyInfo.objects.create(
            name="Harbe Digital Solutions",
            tagline="We build software that helps businesses grow.",
            about="Harbe Digital Solutions is a premier software engineering firm.",
            email="contact@harbedigital.com",
            phone="+1234567890",
            address="123 Tech Street, Silicon Valley",
            facebook="https://facebook.com/harbe",
            linkedin="https://linkedin.com/company/harbe",
            github="https://github.com/harbe",
        )

        # Team member
        self.team_member = TeamMember.objects.create(
            full_name="Jane Doe",
            position="Lead Engineer",
            bio="Passionate software architect with 10+ years experience.",
            email="jane@harbedigital.com",
            is_active=True,
        )

        # FAQ
        self.faq = FAQ.objects.create(
            question="What services do you offer?",
            answer="Web development, mobile apps, and custom software systems.",
        )

        # Services
        self.service_featured = Service.objects.create(
            name="Custom Web Development",
            short_description="High-performance web apps built to scale.",
            description="Detailed description for custom web development services.",
            icon="fa-solid fa-code",
            is_featured=True,
        )
        self.service_non_featured = Service.objects.create(
            name="Cloud Consulting",
            short_description="Cloud migrations and infrastructure automation.",
            description="Detailed cloud consulting service description.",
            icon="fa-solid fa-cloud",
            is_featured=False,
        )

        # Projects
        self.project_featured = Project.objects.create(
            title="Enterprise CRM System",
            client="Acme Corp",
            short_description="A CRM platform tailored to enterprise workflows.",
            description="Comprehensive enterprise CRM built with modern architecture.",
            is_featured=True,
            is_completed=True,
        )
        self.project_image = ProjectImage.objects.create(
            project=self.project_featured,
            caption="Dashboard View",
        )

    def test_home_page(self):
        response = self.client.get(reverse("core:home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "core/home.html")
        self.assertContains(response, "Harbe Digital Solutions")
        self.assertContains(response, "Custom Web Development")
        self.assertContains(response, "Enterprise CRM System")
        self.assertContains(response, "What services do you offer?")

    def test_about_page(self):
        response = self.client.get(reverse("core:about"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "core/about.html")
        self.assertContains(response, "Harbe Digital Solutions")

    def test_services_list_page(self):
        response = self.client.get(reverse("services:list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "services/list.html")
        self.assertContains(response, "Custom Web Development")
        self.assertContains(response, "Cloud Consulting")

    def test_services_detail_page(self):
        response = self.client.get(reverse("services:detail", kwargs={"pk": self.service_featured.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "services/detail.html")
        self.assertContains(response, "Custom Web Development")
        self.assertContains(response, "Detailed description for custom web development services.")

    def test_services_detail_404(self):
        response = self.client.get(reverse("services:detail", kwargs={"pk": 9999}))
        self.assertEqual(response.status_code, 404)

    def test_portfolio_list_page(self):
        response = self.client.get(reverse("portfolio:list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "portfolio/list.html")
        self.assertContains(response, "Enterprise CRM System")
        self.assertContains(response, "Acme Corp")

    def test_portfolio_detail_page(self):
        response = self.client.get(reverse("portfolio:detail", kwargs={"pk": self.project_featured.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "portfolio/detail.html")
        self.assertContains(response, "Enterprise CRM System")
        self.assertContains(response, "Acme Corp")

    def test_portfolio_detail_404(self):
        response = self.client.get(reverse("portfolio:detail", kwargs={"pk": 9999}))
        self.assertEqual(response.status_code, 404)

    def test_contact_page_get(self):
        response = self.client.get(reverse("contact:contact"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "contact/contact.html")
        self.assertContains(response, "Send us a project inquiry")

    def test_contact_page_post_success(self):
        post_data = {
            "name": "Alice Smith",
            "email": "alice@example.com",
            "phone": "+1987654321",
            "company": "Startup Inc",
            "subject": "Project Inquiry",
            "message": "We would like to request a quote for building a SaaS app.",
        }
        response = self.client.post(reverse("contact:contact"), data=post_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Thank you for contacting us! Your message has been received.")
        
        # Verify in database
        self.assertEqual(ContactMessage.objects.count(), 1)
        msg = ContactMessage.objects.first()
        self.assertEqual(msg.name, "Alice Smith")
        self.assertEqual(msg.email, "alice@example.com")
        self.assertEqual(msg.subject, "Project Inquiry")
        self.assertFalse(msg.is_read)

    def test_contact_page_post_invalid(self):
        # Missing required fields like email and message
        post_data = {
            "name": "Alice Smith",
            "email": "not-an-email",
            "subject": "Missing fields",
            "message": "",
        }
        response = self.client.post(reverse("contact:contact"), data=post_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(ContactMessage.objects.count(), 0)
