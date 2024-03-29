from django.contrib import admin
from django.contrib.auth.models import User
from django.forms import TextInput, Widget
from django.utils.html import format_html
from django.db import models

# from django.apps import apps
from pySEZ.utils import opposite_color, get_sentinel_user


class Status(models.Model):
    class Meta:
        verbose_name_plural = "Statuses"
        ordering = ("-state", "name")

    NEW = "NEW"
    PENDING = "PENDING"
    DONE = "DONE"
    CANCELED = "CANCELED"

    STATE_CHOICES = [
        ("NEW", "New"),
        ("PENDING", "Pending"),
        ("DONE", "Done"),
        ("CANCELED", "Canceled"),
    ]

    name = models.CharField(max_length=50)
    color = models.CharField(max_length=7, default="#eeeeee")
    state = models.CharField(max_length=8, choices=STATE_CHOICES, default=NEW)

    def __str__(self):
        return self.name

    @property
    def css_bg_color(self):
        return f"background-color: {self.color}; "

    @property
    def css_text_color(self):
        return f"color: {opposite_color(self.color)}; "

    @admin.display
    def color_code(self):
        return format_html(
            f'<span style="{self.css_bg_color}{self.css_text_color}'
            f' display: block; width: 100%; padding: 3px; text-align: center;">{self.color}</span>'
        )
