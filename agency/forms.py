from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from agency.models import Redactor, Newspaper


class RedactorCreationForm(UserCreationForm):
    class Meta:
        model = Redactor
        fields = UserCreationForm.Meta.fields + ("years_of_experience", "first_name", "last_name",)


class RedactorExperienceUpdateForm(forms.ModelForm):
    years_of_experience = forms.IntegerField()

    class Meta:
        model = Redactor
        fields = ("years_of_experience",)

    def clean_experience_number(self):
        years_of_experience = self.cleaned_data["years_of_experience"]

        if not years_of_experience.isdigit():
            raise ValidationError("Experience should be a digit number")

        if years_of_experience > 35:
            raise ValidationError("Experience should be less than 35")
        return years_of_experience


class NewspaperForm(forms.ModelForm):
    newspapers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        required=False
    )

    class Meta:
        model = Newspaper
        fields = "__all__"


class RedactorUsernameSearchForm(forms.Form):
    username = forms.CharField(
        max_length=63,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by username"})
    )


class NewspaperTitleSearchForm(forms.Form):
    title = forms.CharField(
        max_length=63,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by username"})
    )


class TopicNameSearchForm(forms.Form):
    name = forms.CharField(
        max_length=63,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by name"})
    )
