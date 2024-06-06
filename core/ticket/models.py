from django.db import models
from .validators import validate_iranian_phone_number


class TicketStatus(models.IntegerChoices):
    open = 1, 'در انتظار'
    in_progress = 2, 'در حال پاسخ دهی'
    closed = 3, 'پاسخ داده شده'


class TicketModel(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15, blank=True, null=True,  validators=[
                                    validate_iranian_phone_number])
    description = models.TextField()
    status = models.SmallIntegerField(
        choices=TicketStatus.choices, default=TicketStatus.open)

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created_date',)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    def get_status(self):
        return {
            'id': self.status,
            "title":TicketStatus(self.status).name,
            "label":TicketStatus(self.status).label,
        }


class NewsletterSubscriberModel(models.Model):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email
