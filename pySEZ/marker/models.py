from django.contrib import admin
from django.db import models
from django.utils.html import format_html
from pySEZ.utils import opposite_color

class Marker(models.Model):
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=7,  default='#ee0f0f')
    # orders = models.ManyToManyField(Order)

    def __str__(self):
        return self.name

    @admin.display
    def color_code(self):
        return format_html(f'<span style="background-color: {self.color}; color: {opposite_color(self.color)};'
                           f' display: block; width: 100%; padding: 3px; text-align: center;">{self.color}</span>')