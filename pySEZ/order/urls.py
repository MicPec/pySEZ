from django.urls import path
from . import views

urlpatterns = [
    path("", views.OrderListView.as_view(), name="order_index"),
    path("create/", views.OrderCreateView.as_view(), name="order_create"),
    path("<int:pk>/", views.OrderDetailView.as_view(), name="order_detail"),
    path("<int:pk>/update/", views.OrderUpdateView.as_view(), name="order_update"),
    path("<int:pk>/delete/", views.OrderDeleteView.as_view(), name="order_delete"),
]
