from django.db import models
from django.contrib.auth.models import User
from order.models import Order
from status.models import Status
from pySEZ.utils import get_sentinel_user


class StatusLog(models.Model):
    user = models.ForeignKey(User,
                            #  default=User,
                             on_delete=models.SET(get_sentinel_user))
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    status = models.ForeignKey(Status, on_delete=models.PROTECT)
    date_changed = models.DateTimeField(auto_now_add=True)
    comment = models.CharField(max_length=255, blank=True)
