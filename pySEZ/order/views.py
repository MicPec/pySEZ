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
from .models import Order
from .forms import OrderForm


class OrderListView(ListView):
    model = Order
    ordering = ["-id"]
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
        return ["order/_order_list.html"] if self.request.htmx else ["order/order_list.html"]


class OrderDetailView(DetailView):
    model = Order


class OrderCreateView(CreateView):
    model = Order
    form_class = OrderForm

    def get_success_url(self):
        if self.request.htmx:
            return self.request.META.get("HTTP_REFERER")
        else:
            return reverse_lazy("order-detail", kwargs={"pk": self.object.pk})

    def get_template_names(self):
        return ["scraps/_edit_form.html"] if self.request.htmx else ["edit_form.html"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Nowy Klient"
        context["action"] = reverse('order-create')
        return context


class OrderUpdateView(UpdateView):
    model = Order
    form_class = OrderForm
    extra_context = {"title": "Edycja Klienta"}

    def get_success_url(self):
        # return self.request.META.get("HTTP_REFERER")
        return reverse_lazy("order-list")

    def get_template_names(self):
        return ["scraps/_edit_form.html"] if self.request.htmx else ["edit_form.html"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Edycja Klienta"
        context["action"] = reverse('order-update', args=[self.object.pk])
        return context


class OrderDeleteView(DeleteView):
    model = Order
    success_url = "/orders/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["question"] = "Czy usunąć klienta?"
        context["subject"] = self.object
        context["action"] = reverse('order-delete', args=[self.object.pk])
        return context

    def get_template_names(self):
        return ["scraps/_confirm_delete.html"] if self.request.htmx else ["confirm_delete.html"]
