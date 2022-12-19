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

    def get_queryset(self):
        qs = super().get_queryset()
        if s := self.request.GET.get("search"):
            qs = qs.filter(
                Q(firstname__icontains=s)
                | Q(lastname__icontains=s)
                | Q(company__icontains=s)
            )
        return qs.order_by("lastname",)

    def get_template_names(self):
        return (
            ["client/_client_list.html"]
            if self.request.htmx
            else ["client/client_list.html"]
        )


class ClientDetailView(DetailView):
    model = Client

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        match self.request.GET.get('orders_state'):
            case 'NEW': context["orders_filtered"] = self.object.orders_new
            case 'PENDING': context["orders_filtered"] = self.object.orders_pending
            case 'DONE': context["orders_filtered"] = self.object.orders_done
            case _: context["orders_filtered"] = self.object.orders.all()
        return context


class ClientCreateView(CreateView):
    model = Client
    form_class = ClientForm

    def get_success_url(self):
        if self.request.htmx:
            return self.request.META.get("HTTP_REFERER")
        else:
            return reverse_lazy("client-detail", kwargs={"pk": self.object.pk})

    def get_template_names(self):
        return ["scraps/_edit_form.html"] if self.request.htmx else ["edit_form.html"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "New client"
        context["action"] = reverse("client-create")
        return context


class ClientUpdateView(UpdateView):
    model = Client
    form_class = ClientForm

    def get_success_url(self):
        return self.request.META.get("HTTP_REFERER")
        # return reverse_lazy("client-list")

    def get_template_names(self):
        return ["scraps/_edit_form.html"] if self.request.htmx else ["edit_form.html"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Edit client"
        context["action"] = reverse("client-update", args=[self.object.pk])
        return context


class ClientDeleteView(DeleteView):
    model = Client
    success_url = "/clients/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["question"] = "Delete client?"
        context["subject"] = self.object
        context["action"] = reverse("client-delete", args=[self.object.pk])
        return context

    def get_template_names(self):
        return (
            ["scraps/_confirm_delete.html"]
            if self.request.htmx
            else ["confirm_delete.html"]
        )
