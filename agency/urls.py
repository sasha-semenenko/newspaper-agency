from django.urls import path

from agency.views import (index,
                          TopicListView,
                          NewspaperListView,
                          NewspaperDetailView,
                          RedactorListView,
                          RedactorDetailView,
                          TopicCreateView,
                          TopicUpdateView,
                          TopicDeleteView,
                          NewspaperCreateView,
                          NewspaperUpdateView,
                          NewspaperDeleteView,
                          RedactorCreateView,
                          RedactorDeleteView,
                          RedactorExperienceUpdateView,
                          NewspaperUpdateRedactorView)

urlpatterns = [
    path("", index, name="index"),
    path("topics/", TopicListView.as_view(), name="topics"),
    path("newspaper/", NewspaperListView.as_view(), name="newspaper"),
    path("newspaper/<int:pk>/", NewspaperDetailView.as_view(), name="newspaper-detail"),
    path("redactors/", RedactorListView.as_view(), name="redactors"),
    path("redactors/<int:pk>/", RedactorDetailView.as_view(), name="redactor-detail"),
    path("topics/create/", TopicCreateView.as_view(), name="topic-create"),
    path("topics/<int:pk>/update/", TopicUpdateView.as_view(), name="topic-update"),
    path("topics/<int:pk>/delete/", TopicDeleteView.as_view(), name="topic-delete"),
    path("newspaper/create/", NewspaperCreateView.as_view(), name="newspaper-create"),
    path("newspaper/<int:pk>/update/", NewspaperUpdateView.as_view(), name="newspaper-update"),
    path("newspaper/<int:pk>/delete/", NewspaperDeleteView.as_view(), name="newspaper-delete"),
    path("redactor/create/", RedactorCreateView.as_view(), name="redactor-create"),
    path("redactor/<int:pk>/delete/", RedactorDeleteView.as_view(), name="redactor-delete"),
    path("redactor/<int:pk>/update", RedactorExperienceUpdateView.as_view(), name="redactor-experience-update"),
    path("redactor/<int:pk>/update/redactor/", NewspaperUpdateRedactorView.as_view(), name="newspaper-update-redactor")

]

app_name = "agency"
