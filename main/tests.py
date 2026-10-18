from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

class HomePageTests(TestCase):
    def test_homepage_renders_without_optional_profile_files(self):
        User.objects.create_user(username="portfolio-owner")

        response = self.client.get(reverse("main:home"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'src="/static/css/images/icon.jpg"')
        self.assertNotContains(response, "Download Resume")

    def test_homepage_hides_literal_none_profile_title(self):
        user = User.objects.create_user(username="portfolio-owner")
        user.userprofile.title = "None"
        user.userprofile.save()

        response = self.client.get(reverse("main:home"))

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Backend Developer None")
