from django.contrib.auth import get_user_model
from django.test import TestCase
from agency.models import Topic, Newspaper


class ModelsTests(TestCase):
    def test_topic_str(self):
        topic = Topic.objects.create(name="crime")
        self.assertEquals(str(topic), f"{topic.name}")

    def test_newspaper_str(self):
        title = "Bitcoin is the most treasure in the world?"
        published_date = "2023-01-01"
        name = "Trade"
        topic = Topic.objects.create(name=name)
        newspaper = Newspaper.objects.create(title=title, published_date=published_date, topic=topic)
        self.assertEquals(str(newspaper), f"{newspaper.title} published at {newspaper.published_date}")

    def test_create_redactor_with_experience(self):
        username = "kononenko78"
        password = "qaz1257wsx"
        years_of_experience = 3
        redactor = get_user_model().objects.create_user(
            username=username,
            password=password,
            years_of_experience=years_of_experience
        )
        self.assertEquals(redactor.username, username)
        self.assertTrue(redactor.check_password(password))
        self.assertEquals(redactor.years_of_experience, years_of_experience)
