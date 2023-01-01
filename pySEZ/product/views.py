from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .forms import ProductForm
from .models import Product


class ProductListView(LoginRequiredMixin, ListView):
    model = Product
    ordering = ["name"]
    paginate_by = 10

    def get_queryset(self):
        query = super().get_queryset()
        if s := self.request.GET.get("search"):
            query = query.filter(name__icontains=s)
        return query

    def get_template_names(self):
        return (
            ["product/_product_list.html"]
            if self.request.htmx
            else ["product/product_list.html"]
        )


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm

    def get_success_url(self):
        if self.request.htmx:
            return self.request.META.get("HTTP_REFERER")
        else:
            return reverse_lazy("product-detail", kwargs={"pk": self.object.pk})

    def get_template_names(self):
        return ["scraps/_edit_form.html"] if self.request.htmx else ["edit_form.html"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Nowy Produkt"
        context["action"] = reverse("product_create")
        return context


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm

    def get_success_url(self):
        # return self.request.META.get("HTTP_REFERER")
        return reverse_lazy("product-list")

    def get_template_names(self):
        return ["scraps/_edit_form.html"] if self.request.htmx else ["edit_form.html"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Edit product"
        context["action"] = reverse("product-update", args=[self.object.pk])
        return context


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["question"] = "Delete product?"
        context["subject"] = self.object
        context["action"] = reverse("product-delete", args=[self.object.pk])
        return context

    def get_template_names(self):
        return (
            ["scraps/_confirm_delete.html"]
            if self.request.htmx
            else ["confirm_delete.html"]
        )

    def get_success_url(self):
        return self.request.META.get("HTTP_REFERER")
        # return reverse_lazy("product-list")
