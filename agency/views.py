from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import generic

from agency.forms import (NewspaperForm,
                          RedactorCreationForm,
                          RedactorExperienceUpdateForm,
                          TopicNameSearchForm,
                          NewspaperTitleSearchForm,
                          RedactorUsernameSearchForm)
from agency.models import Topic, Newspaper, Redactor


def index(request):
    num_topic = Topic.objects.count()
    num_newspapers = Newspaper.objects.count()
    num_redactors = Redactor.objects.count()

    context = {
        "num_topic": num_topic,
        "num_newspapers": num_newspapers,
        "num_redactors": num_redactors,
    }

    return render(request, "agency/index.html", context=context)


class TopicListView(LoginRequiredMixin, generic.ListView):
    model = Topic
    queryset = Topic.objects.all()
    template_name = "agency/topic_list.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TopicListView, self).get_context_data(**kwargs)
        context["search_form"] = TopicNameSearchForm()
        return context

    def get_queryset(self):
        form = TopicNameSearchForm(self.request.GET)
        if form.is_valid():
            return self.queryset.filter(name__icontains=form.cleaned_data["name"])
        return self.queryset


class NewspaperListView(LoginRequiredMixin, generic.ListView):
    model = Newspaper
    queryset = Newspaper.objects.select_related("topic")
    template_name = "agency/newspaper_list.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(NewspaperListView, self).get_context_data(**kwargs)
        context["search_form"] = NewspaperTitleSearchForm()
        return context

    def get_queryset(self):
        form = NewspaperTitleSearchForm(self.request.GET)
        if form.is_valid():
            return self.queryset.filter(title__icontains=form.cleaned_data["title"])
        return self.queryset

class NewspaperDetailView(LoginRequiredMixin, generic.DetailView):
    model = Newspaper


class RedactorListView(LoginRequiredMixin, generic.ListView):
    model = Redactor

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(RedactorListView, self).get_context_data(**kwargs)
        context["search_form"] = RedactorUsernameSearchForm()
        return context

    def get_queryset(self):
        queryset = Redactor.objects.all()
        form = RedactorUsernameSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(username__icontains=form.cleaned_data["username"])
        return queryset

class RedactorDetailView(LoginRequiredMixin, generic.DetailView):
    model = Redactor
    queryset = Redactor.objects.prefetch_related("newspaper_set__topic")


class TopicCreateView(LoginRequiredMixin, generic.CreateView):
    model = Topic
    fields = "__all__"
    success_url = reverse_lazy("agency:topics")


class TopicUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Topic
    fields = "__all__"
    success_url = reverse_lazy("agency:topics")


class TopicDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Topic
    success_url = reverse_lazy("agency:topics")
    template_name = "agency/topic_confirm_delete.html"


class NewspaperCreateView(LoginRequiredMixin, generic.CreateView):
    model = Newspaper
    form_class = NewspaperForm
    success_url = reverse_lazy("agency:newspaper")


class NewspaperUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Newspaper
    form_class = NewspaperForm
    success_url = reverse_lazy("agency:newspaper")


class NewspaperDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Newspaper
    template_name = "agency/newspaper_confirm_delete.html"
    success_url = reverse_lazy("agency:newspaper")


class RedactorCreateView(LoginRequiredMixin, generic.CreateView):
    model = Redactor
    form_class = RedactorCreationForm
    success_url = reverse_lazy("agency:redactors")


class RedactorDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Redactor
    success_url = reverse_lazy("agency:redactors")


class RedactorExperienceUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Redactor
    form_class = RedactorExperienceUpdateForm
    template_name = "agency/redactor_update.html"
    success_url = reverse_lazy("agency:redactors")


class NewspaperUpdateRedactorView(LoginRequiredMixin, generic.UpdateView):
    def post(self, request, *args, **kwargs):
        redactor = request.user
        newspaper = get_object_or_404(Newspaper, pk=kwargs["pk"])
        if redactor in newspaper.publishers.all():
            newspaper.publishers.remove(redactor)
        else:
            newspaper.publishers.add(redactor)
        return redirect("agency:newspaper-detail", pk=kwargs["pk"])
