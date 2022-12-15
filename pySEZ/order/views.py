from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)
from django_filters.views import FilterView

from order.filters import OrderFilter
from status.models import Status

from .forms import OrderForm, OrderStatusUpdate
from .models import Order


class OrderListView(FilterView):
    model = Order
    ordering = ["-status__state", "-deadline", "-date_created"]
    paginate_by = 5
    filterset_class = OrderFilter

    def get_queryset(self):
        qs = super().get_queryset()
        f = OrderFilter(self.request.GET, queryset=qs)
        qs = f.qs
        if s := self.request.GET.get("search"):
            qs = qs.filter(
                Q(client__firstname__icontains=s)
                | Q(client__lastname__icontains=s)
                | Q(client__company__icontains=s)
                | Q(note__icontains=s)
            )
        return qs

    def get_template_names(self):
        return (
            ["order/_order_list.html"]
            if self.request.htmx
            else ["order/order_list.html"]
        )


class OrderDetailView(DetailView):
    model = Order


class OrderCreateView(CreateView):
    model = Order
    form_class = OrderForm

    def get_success_url(self):
        if self.request.htmx:
            return self.request.META.get("HTTP_REFERER")
        return reverse_lazy("order-detail", kwargs={"pk": self.object.pk})

    def get_template_names(self):
        return ["scraps/_edit_form.html"] if self.request.htmx else ["edit_form.html"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Nowy Klient"
        context["action"] = reverse("order-create")
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.status = Status.objects.filter(state="NEW").first()
        return super(OrderCreateView, self).form_valid(form)


class OrderUpdateView(UpdateView):
    model = Order
    form_class = OrderForm
    extra_context = {"title": "Edycja Klienta"}

    def get_success_url(self):
        return self.request.META.get("HTTP_REFERER")

        if self.request.htmx:
            return self.request.META.get("HTTP_REFERER")
        return reverse_lazy("order-detail", kwargs={"pk": self.object.pk})

    def get_template_names(self):
        return ["scraps/_edit_form.html"] if self.request.htmx else ["edit_form.html"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Order Edit"
        context["action"] = reverse("order-update", args=[self.object.pk])
        # context["next"] =  self.request.META.get("HTTP_REFERER")
        return context


class OrderStatusUpdateView(OrderUpdateView):
    form_class = OrderStatusUpdate
    extra_context = {"title": "Status Change"}

    def get_success_url(self):
        return self.request.META.get("HTTP_REFERER")
        # return reverse_lazy("order-list")

    def get_template_names(self):
        return ["scraps/_edit_form.html"] if self.request.htmx else ["edit_form.html"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Change status"
        context["action"] = reverse("order-status-update", args=[self.object.pk])
        return context


class OrderDeleteView(DeleteView):
    model = Order
    success_url = "/orders/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["question"] = "Do you want to delete the order?"
        context["subject"] = self.object
        context["action"] = reverse("order-delete", args=[self.object.pk])
        return context

    def get_template_names(self):
        return (
            ["scraps/_confirm_delete.html"]
            if self.request.htmx
            else ["confirm_delete.html"]
        )
