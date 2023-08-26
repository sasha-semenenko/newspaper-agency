from django.test import TestCase

from agency.forms import RedactorCreationForm


class FormSTests(TestCase):
    def test_redactor_creation_form(self):
        data = {
            "username": "o_sydorenko",
            "password1": "qwe56qef9",
            "password2": "qwe56qef9",
            "first_name": "Oleg",
            "last_name": "Sydorenko",
            "years_of_experience": 3
        }
        form = RedactorCreationForm(data=data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, data)
