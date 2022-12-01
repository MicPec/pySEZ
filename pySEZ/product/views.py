from django.shortcuts import render
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.urls import reverse_lazy, reverse
from .models import Product
from .forms import ProductForm


class ProductListView(ListView):
    model = Product
    ordering = ["name"]
    paginate_by = 5
    # template_name = ''

    def get_queryset(self):
        query = super().get_queryset()
        if s := self.request.GET.get("search"):
            query = query.filter(name__icontains=s)
        return query

    def get_template_names(self):
       return ["product/_product_list.html"] if self.request.htmx else ["product/product_list.html"]


class ProductDetailView(DetailView):
    model = Product


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm

    def get_success_url(self):
        if self.request.htmx:
            return self.request.META.get("HTTP_REFERER")
        else:
            return reverse_lazy("product_detail", kwargs={"pk": self.object.pk})

    def get_template_names(self):
        return ["scraps/_edit_form.html"] if self.request.htmx else ["edit_form.html"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Nowy Produkt"
        context["action"] = reverse('product_create')
        return context


class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    extra_context = {"title": "Edycja Produktu"}

    def get_success_url(self):
        # return self.request.META.get("HTTP_REFERER")
        return reverse_lazy("product_index")

    def get_template_names(self):
        return ["scraps/_edit_form.html"] if self.request.htmx else ["edit_form.html"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Edycja Produktu"
        context["action"] = reverse('product_update', args=[self.object.pk])
        return context


class ProductDeleteView(DeleteView):
    model = Product
    success_url = "/products/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["question"] = "Czy usunąć produkt ?"
        context["subject"] = self.object
        context["action"] = reverse('product_delete', args=[self.object.pk])
        return context

    def get_template_names(self):
        return ["scraps/_confirm_delete.html"] if self.request.htmx else ["confirm_delete.html"]
