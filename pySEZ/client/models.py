from django.db import models
from django.shortcuts import redirect


class Client(models.Model):
    firstname = models.CharField(max_length=50, blank=True)
    lastname = models.CharField(max_length=50)
    email = models.EmailField(max_length=150, unique=True)
    phone = models.CharField(max_length=20)
    company = models.CharField(max_length=50, blank=True)
    website = models.URLField(max_length=150, blank=True)

    def __str__(self):
        company = f"({self.company})" if self.company != "" else ""
        return f"{self.fullname} {company}"

    def get_absolute_url(self):
        return redirect("client-detail", pk=self.pk)

    @property
    def fullname(self, reverse=True):
        return f'{self.lastname} {self.firstname}' if reverse else f'{self.firstname} {self.lastname}'
