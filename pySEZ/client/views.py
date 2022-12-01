from django.shortcuts import render, redirect
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.db.models import Q
from django.urls import reverse_lazy, reverse
from .models import Client
from .forms import ClientForm


class ClientListView(ListView):
    model = Client
    ordering = ["lastname"]
    paginate_by = 5
    # template_name = ''

    def get_queryset(self):
        query = super().get_queryset()
        if s := self.request.GET.get("search"):
            query = query.filter(
                Q(firstname__icontains=s)
                | Q(lastname__icontains=s)
                | Q(company__icontains=s)
            )
        return query

    def get_template_names(self):
        return ["client/_client_list.html"] if self.request.htmx else ["client/client_list.html"]


class ClientDetailView(DetailView):
    model = Client


class ClientCreateView(CreateView):
    model = Client
    form_class = ClientForm

    def get_success_url(self):
        if self.request.htmx:
            return self.request.META.get("HTTP_REFERER")
        else:
            return reverse_lazy("client_detail", kwargs={"pk": self.object.pk})

    def get_template_names(self):
        return ["scraps/_edit_form.html"] if self.request.htmx else ["edit_form.html"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Nowy Klient"
        context["action"] = reverse('client_create')
        return context


class ClientUpdateView(UpdateView):
    model = Client
    form_class = ClientForm
    extra_context = {"title": "Edycja Klienta"}

    def get_success_url(self):
        # return self.request.META.get("HTTP_REFERER")
        return reverse_lazy("client_index")

    def get_template_names(self):
        return ["scraps/_edit_form.html"] if self.request.htmx else ["edit_form.html"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Edycja Klienta"
        context["action"] = reverse('client_update', args=[self.object.pk])
        return context


class ClientDeleteView(DeleteView):
    model = Client
    success_url = "/clients/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["question"] = "Czy usunąć klienta?"
        context["subject"] = self.object
        context["action"] = reverse('client_delete', args=[self.object.pk])
        return context

    def get_template_names(self):
        return ["scraps/_confirm_delete.html"] if self.request.htmx else ["confirm_delete.html"]
