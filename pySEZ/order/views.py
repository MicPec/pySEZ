from copy import copy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.forms import ModelForm
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, UpdateView
from django_filters.views import FilterView
from order.filters import OrderFilter
from status.models import Status
from status_log.models import StatusLog

from .forms import OrderForm, OrderItemForm, OrderStatusUpdate
from .models import Order, OrderItem


class OrderListView(LoginRequiredMixin, FilterView):
    model = Order
    ordering = ["-status__state", "-deadline", "-date_created"]
    paginate_by = 10
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
        return qs.order_by("-status__state", "-deadline", "-date_created")

    def get_template_names(self):
        return (
            ["order/_order_list.html"]
            if self.request.htmx
            else ["order/order_list.html"]
        )


class OrderDetailView(LoginRequiredMixin, DetailView):
    model = Order

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["statuslog"] = StatusLog.objects.filter(order=self.object).order_by(
            "-date_changed"
        )
        return context


class OrderCreateView(LoginRequiredMixin, CreateView):
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
        context["title"] = "New Client"
        context["action"] = reverse("order-create")
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.status = Status.objects.filter(state="NEW").first()
        return super().form_valid(form)


class OrderItemCreateView(LoginRequiredMixin, CreateView):
    model = OrderItem
    form_class = OrderItemForm

    def get_success_url(self):
        if self.request.htmx:
            return self.request.META.get("HTTP_REFERER")
        return reverse_lazy("order-detail", kwargs={"pk": self.object.order.pk})

    def get_template_names(self):
        return ["scraps/_edit_form.html"] if self.request.htmx else ["edit_form.html"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "New Item"
        context["action"] = reverse("orderitem-create", args=[self.kwargs["pk"]])
        return context

    def get_status_logger(self, form, comment: str = "") -> StatusLog:
        return StatusLog(
            user=self.request.user,
            order=form.instance.order,
            status=form.instance.order.status,
            comment=comment,
        )

    def form_valid(self, form):
        form.instance.order = Order.objects.get(pk=self.kwargs["pk"])
        self.get_status_logger(form, f"Order item added: {form.instance}").save()
        return super().form_valid(form)


class OrderItemUpdateView(LoginRequiredMixin, UpdateView):
    model = OrderItem
    form_class = OrderItemForm

    def get_success_url(self):
        if self.request.htmx:
            return self.request.META.get("HTTP_REFERER")
        return reverse_lazy("order-detail", kwargs={"pk": self.object.order.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Update Item"
        context["action"] = reverse("orderitem-update", args=[self.kwargs["pk"]])
        return context

    def get_template_names(self):
        return ["scraps/_edit_form.html"] if self.request.htmx else ["edit_form.html"]

    def get_status_logger(self, form, comment: str = "") -> StatusLog:
        return StatusLog(
            user=self.request.user,
            order=form.instance.order,
            status=form.instance.order.status,
            comment=comment,
        )

    def get_object(self, queryset=None):
        object = super().get_object(queryset)
        self.before = copy(object)
        return object

    def form_valid(self, form):
        # form.instance.order = Order.objects.get(pk=self.kwargs["pk"])
        if self.before.product.pk == form.instance.product.pk:
            msg = f"Order item changed: {form.instance}"
        else:
            msg = f"Order item changed: {self.before.product} -> {form.instance}"
        self.get_status_logger(form, msg).save()
        return super().form_valid(form)


class OrderItemDeleteView(LoginRequiredMixin, DeleteView):
    model = OrderItem

    def get_success_url(self) -> str:
        return reverse_lazy("order-detail", kwargs={"pk": self.object.order.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["question"] = "Do you want to delete the item?"
        context["subject"] = self.object
        context["action"] = reverse("orderitem-delete", args=[self.kwargs["pk"]])
        return context

    def get_template_names(self):
        return (
            ["scraps/_confirm_delete.html"]
            if self.request.htmx
            else ["confirm_delete.html"]
        )

    def get_status_logger(self, comment: str = "") -> StatusLog:
        return StatusLog(
            user=self.request.user,
            order=self.object.order,
            status=self.object.order.status,
            comment=comment,
        )

    def form_valid(self, form):
        # form.instance.order = Order.objects.get(pk=self.kwargs["pk"])
        self.get_status_logger(f"Order item deleted: {self.object}").save()
        return super().form_valid(form)


class OrderUpdateView(LoginRequiredMixin, UpdateView):
    model = Order
    form_class = OrderForm

    def get_success_url(self):
        return reverse_lazy("order-detail", kwargs={"pk": self.object.pk})

    def get_template_names(self):
        return ["scraps/_edit_form.html"] if self.request.htmx else ["edit_form.html"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = f"Edit Order: #{self.object.pk}"
        context["action"] = reverse("order-update", args=[self.object.pk])
        return context

    def get_status_logger(self, form: ModelForm, comment: str = "") -> StatusLog:
        # log changes to order
        if not hasattr(self, "_status_log"):
            self._status_log = StatusLog(
                user=self.request.user,
                order=self.object,
                status=form.instance.status,
                comment=comment,
            )
        return self._status_log

    def form_valid(self, form):
        # form.instance.user = self.request.user
        logger = self.get_status_logger(form, "Order changed")
        logger.save()

        return super().form_valid(form)


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
        context["title"] = f"Change status for order: #{self.object.pk}"
        context["action"] = reverse("order-status-update", args=[self.object.pk])
        return context

    def form_valid(self, form):
        self.get_status_logger(
            form, form.cleaned_data["comment"] or "Order status changed."
        ).save()
        return super().form_valid(form)


class OrderDeleteView(LoginRequiredMixin, DeleteView):
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
