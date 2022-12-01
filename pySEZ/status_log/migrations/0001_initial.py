# Generated by Django 4.1.3 on 2022-11-19 17:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import pySEZ.utils


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('order', '0001_initial'),
        ('status', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='StatusLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_changed', models.DateTimeField(auto_now_add=True)),
                ('comment', models.CharField(blank=True, max_length=255)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='order.order')),
                ('status', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='status.status')),
                ('user', models.ForeignKey(on_delete=models.SET(pySEZ.utils.get_sentinel_user), to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
