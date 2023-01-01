from django.urls import path
from . import views

urlpatterns = [
    path("", views.OrderListView.as_view(), name="order-list"),
    path("create/", views.OrderCreateView.as_view(), name="order-create"),
    path("<int:pk>/", views.OrderDetailView.as_view(), name="order-detail"),
    path("<int:pk>/update/", views.OrderUpdateView.as_view(), name="order-update"),
    path(
        "<int:pk>/status-update/",
        views.OrderStatusUpdateView.as_view(),
        name="order-status-update",
    ),
    path("<int:pk>/delete/", views.OrderDeleteView.as_view(), name="order-delete"),
    path(
        "<int:pk>/add-orderitem/",
        views.OrderItemCreateView.as_view(),
        name="orderitem-create",
    ),
    path(
        "update-orderitem/<int:pk>",
        views.OrderItemUpdateView.as_view(),
        name="orderitem-update",
    ),
    path(
        "delete-orderitem/<int:pk>",
        views.OrderItemDeleteView.as_view(),
        name="orderitem-delete",
    ),
]
