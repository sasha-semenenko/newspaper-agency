from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from agency.models import Topic, Newspaper, Redactor

TOPIC_LIST_URL = reverse("agency:topics")
NEWSPAPER_LIST_URL = reverse("agency:newspaper")
REDACTOR_LIST_URL = reverse("agency:redactors")


class PublicTopicTests(TestCase):
    def test_login_required(self):
        response = self.client.get(TOPIC_LIST_URL)
        self.assertNotEquals(response.status_code, 200)


class PrivateTopicTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="moroz968",
            password="rfv578tgh"
        )
        self.client.force_login(self.user)

    def test_retrieve_topic(self):
        Topic.objects.create(name="politics")
        Topic.objects.create(name="art")
        response = self.client.get(TOPIC_LIST_URL)
        topic = Topic.objects.all()
        self.assertEquals(response.status_code, 200)
        self.assertEquals(list(response.context["topic_list"]), list(topic))
        self.assertTemplateUsed(response, "agency/topic_list.html")

    def test_topic_search(self):
        Topic.objects.create(name="crime")
        response = self.client.get(TOPIC_LIST_URL)
        search = Topic.objects.filter(name="crime")
        self.assertEquals(response.status_code, 200)
        self.assertEquals(list(response.context["topic_list"]), list(search))


class PublicNewspaperTests(TestCase):
    def test_login_required(self):
        response = self.client.get(NEWSPAPER_LIST_URL)
        self.assertNotEquals(response.status_code, 200)


class PrivateNewspaperTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="black_adam86",
            password="plok964qaz"
        )
        self.client.force_login(self.user)

    def test_retrieve_newspaper(self):
        topic = Topic.objects.create(name="business")
        Newspaper.objects.create(
            topic=topic,
            published_date="2023-02-02",
            title="The Government of Ukraine will raise the working day for the people")
        response = self.client.get(NEWSPAPER_LIST_URL)
        newspaper = Newspaper.objects.all()
        self.assertEquals(response.status_code, 200)
        self.assertEquals(list(response.context["newspaper_list"]), list(newspaper))

    def test_search_newspaper(self):
        topic = Topic.objects.create(name="travel")
        Newspaper.objects.create(
            topic=topic,
            published_date="2023-03-03",
            title="10 most beautiful places in the Ukraine, which you have visited")
        response = self.client.get(NEWSPAPER_LIST_URL)
        newspaper = Newspaper.objects.filter(title="10 most beautiful places in the Ukraine, which you have visited")
        self.assertEquals(response.status_code, 200)
        self.assertEquals(list(response.context["newspaper_list"]), list(newspaper))


class PublicRedactorTests(TestCase):
    def test_login_required(self):
        response = self.client.get(REDACTOR_LIST_URL)
        self.assertNotEquals(response.status_code, 200)


class PrivateRedactorTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="black_widow57",
            password="fvgre6894er"
        )
        self.client.force_login(self.user)

    def test_retrieve_redactor(self):
        get_user_model().objects.create(
            username="o_moroz123",
            first_name="Oleksandr",
            last_name="Moroz",
            years_of_experience=3
        )
        get_user_model().objects.create(
            username="d_onstap78",
            first_name="Dmytro",
            last_name="Ostapenko",
            years_of_experience=5
        )
        response = self.client.get(REDACTOR_LIST_URL)
        redactors = Redactor.objects.all()
        self.assertEquals(response.status_code, 200)
        self.assertEquals(list(response.context["redactor_list"]), list(redactors))

    def test_search_redactor(self):
        response = self.client.get(REDACTOR_LIST_URL, {"username": "o_sydor242"})
        search = get_user_model().objects.filter(username="o_sydor242")
        self.assertEquals(response.status_code, 200)
        self.assertEquals(list(response.context["redactor_list"]), list(search))
