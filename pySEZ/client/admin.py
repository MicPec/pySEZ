from django.contrib import admin
from .models import Client


@admin.register(Client)
class ClientInfo(admin.ModelAdmin):
    list_display = (
        "lastname",
        "firstname",
        "company",
        "email",
        "phone",
        "website",
    )
    fieldsets = (
        ("Dane", {"fields":
            ("firstname", "lastname", "company")}),
        ("Kontakt", {"fields":
            ("email", "phone", "website")}),
    )
    search_fields = ("firstname", "lastname", "company")
