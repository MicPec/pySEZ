from django.urls import path
from . import views

urlpatterns = [
    path("", views.OrderListView.as_view(), name="order-list"),
    path("create/", views.OrderCreateView.as_view(), name="order-create"),
    path("<int:pk>/", views.OrderDetailView.as_view(), name="order-detail"),
    path("<int:pk>/update/", views.OrderUpdateView.as_view(), name="order-update"),
    path("<int:pk>/status-update/", views.OrderStatusUpdateView.as_view(), name="order-status-update"),
    path("<int:pk>/delete/", views.OrderDeleteView.as_view(), name="order-delete"),
]
