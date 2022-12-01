from django.contrib import admin
from django.contrib.auth.models import User
from django.utils.html import format_html
from django.db import models
# from django.apps import apps
from pySEZ.utils import opposite_color, get_sentinel_user


class Status(models.Model):
    NOT_SET = 'NOT_SET'
    NEW = 'NEW'
    PROGRESS = 'PROGRESS'
    DONE = 'DONE'

    STATE_CHOICES = [
        ('NOT_SET', ''),
        ('NEW', 'New'),
        ('PROGRESS', 'In progress'),
        ('DONE', 'Done'),
    ]

    name = models.CharField(max_length=50)
    color = models.CharField(max_length=7, default='#eeeeee')
    state = models.CharField(max_length=8,
                             choices=STATE_CHOICES,
                             default=NOT_SET)

    def __str__(self):
        return self.name

    @admin.display
    def color_code(self):
        return format_html(
            f'<span style="background-color: {self.color}; color: {opposite_color(self.color)};'
            f' display: block; width: 100%; padding: 3px; text-align: center;">{self.color}</span>'
        )


