from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse


class AdminSiteTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="t_taras59",
            password="rnrt64re"
        )
        self.client.force_login(self.admin_user)
        self.redactor = get_user_model().objects.create_user(
            username="a_andriy24",
            password="tbjy168",
            years_of_experience=7
        )

    def test_list_display(self):
        url = reverse("admin:agency_redactor_changelist")
        response = self.client.get(url)
        self.assertContains(response, self.redactor.years_of_experience)

    def test_detail_display(self):
        url = reverse("admin:agency_redactor_change", args=[self.redactor.id])
        response = self.client.get(url)
        self.assertContains(response, self.redactor.years_of_experience)
