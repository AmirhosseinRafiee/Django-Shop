from django.db import models
from .validators import validate_iranian_phone_number


class TicketStatus(models.IntegerChoices):
    OPEN = 1, 'Open'
    IN_PROGRESS = 2, 'In Progress'
    CLOSED = 3, 'Closed'


class TicketModel(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15, blank=True, null=True,  validators=[
                                    validate_iranian_phone_number])
    description = models.TextField()
    status = models.SmallIntegerField(
        choices=TicketStatus.choices, default=TicketStatus.OPEN)

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class NewsletterSubscriberModel(models.Model):
    email = models.EmailField(unique=True)

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email
