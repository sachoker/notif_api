import pytz
from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone
from django_prometheus.models import ExportModelOperationsMixin


class Mailing(ExportModelOperationsMixin('mailing'), models.Model):
    date_start = models.DateTimeField(verbose_name="Mailing start")
    date_end = models.DateTimeField(verbose_name="Mailing end")
    time_start = models.TimeField(verbose_name="Start time for sending message")
    time_end = models.TimeField(verbose_name="End time for sending message")
    text = models.TextField(max_length=255, verbose_name="Message text")
    tag = models.CharField(max_length=100, verbose_name="Search by tags", blank=True)
    mobile_operator_code = models.CharField(
        verbose_name="Search by mobile operator code", max_length=3, blank=True
    )

    @property
    def to_send(self) -> bool:
        return bool(self.date_start <= timezone.now() <= self.date_end)

    def __str__(self):
        return f"Mailing {self.id} from {self.date_start}"

    class Meta:
        verbose_name = "Mailing"
        verbose_name_plural = "Mailings"


class Client(ExportModelOperationsMixin('client'), models.Model):
    TIMEZONES = tuple(zip(pytz.all_timezones, pytz.all_timezones))

    phone_regex = RegexValidator(
        regex=r"^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$",
        message="The client's phone number must be valid",
    )
    phone_number = models.CharField(
        verbose_name="Phone number",
        validators=[phone_regex],
        unique=True,
        max_length=11,
    )
    mobile_operator_code = models.CharField(
        verbose_name="Mobile operator code", max_length=3, editable=False
    )
    tag = models.CharField(verbose_name="Search tags", max_length=100, blank=True)
    timezone = models.CharField(
        verbose_name="Time zone", max_length=32, choices=TIMEZONES, default="UTC"
    )

    def save(self, *args, **kwargs):
        self.mobile_operator_code = str(self.phone_number)[1:4]
        return super(Client, self).save(*args, **kwargs)

    def __str__(self):
        return f"Client {self.id} with number {self.phone_number}"

    class Meta:
        verbose_name = "Client"
        verbose_name_plural = "Clients"


class Message(ExportModelOperationsMixin('message'), models.Model):
    SENT = "sent"
    NO_SENT = "no sent"

    STATUS_CHOICES = [
        (SENT, "Sent"),
        (NO_SENT, "No sent"),
    ]

    creation_time = models.DateTimeField(verbose_name="Creation time", auto_now_add=True)
    sending_status = models.CharField(
        verbose_name="Sending status", max_length=15, choices=STATUS_CHOICES
    )
    mailing = models.ForeignKey(
        Mailing, on_delete=models.CASCADE, related_name="messages"
    )
    client = models.ForeignKey(
        Client, on_delete=models.CASCADE, related_name="messages"
    )

    def __str__(self):
        return f"Message {self.id} with text {self.mailing} for {self.client}"

    class Meta:
        verbose_name = "Message"
        verbose_name_plural = "Messages"
