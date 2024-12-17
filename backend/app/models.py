from datetime import timedelta
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import UserManager
from django.utils.timezone import now


class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    is_superuser = models.BooleanField(default=False)
    is_organizer = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=15, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    objects = UserManager()

    def __str__(self):
        return f"User {self.name} with email {self.email}"

class Organizer(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    phone_number = models.CharField(max_length=15, null=True)
    description = models.TextField()
    manager = models.ForeignKey(User, on_delete=models.CASCADE)
    is_company = models.BooleanField(default=False)
    company_registration_number = models.CharField(max_length=255, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Organizer {self.name} by {self.manager}"

class Location(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    capacity = models.IntegerField()
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Location {self.name} in {self.city}, {self.country}"

class EventCategories(models.TextChoices):
    MUSIC = 'MUSIC', 'Music'
    SPORTS = 'SPORTS', 'Sports'
    ARTS = 'ARTS', 'Arts'
    FOOD = 'FOOD', 'Food'
    CHARITY = 'CHARITY', 'Charity'
    EDUCATION = 'EDUCATION', 'Education'
    BUSINESS = 'BUSINESS', 'Business'
    TECH = 'TECH', 'Tech'

class Event(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=EventCategories.choices)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    organizer = models.ForeignKey(Organizer, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Event {self.name} by {self.organizer} at {self.location}"

class Ticket(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, default=None)
    sector = models.CharField(max_length=50)
    row = models.CharField(max_length=10)
    seat = models.IntegerField()
    is_reserved = models.BooleanField(default=False)

class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tickets = models.ManyToManyField(Ticket)
    reserved_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(default=None, null=False)
    is_finalized = models.BooleanField(default=False)

    def release(self):
        if self.expires_at < now():
            for ticket in self.tickets.all():
                ticket.is_reserved = False
                ticket.save()
            self.delete()

    def save(self, *args, **kwargs):
        if not self.expires_at:
            self.expires_at = now() + timedelta(minutes=10)
        super().save(*args, **kwargs)

class Payment(models.Model):
    reservation = models.ForeignKey(Reservation, on_delete=models.RESTRICT)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = ['CREDIT_CARD', 'STRIPE', 'AT_LOCATION']
    payment_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Payment for reservation {self.reservation} with total {self.total}"

class Coupon(models.Model):
    code = models.CharField(max_length=50)
    discount = models.DecimalField(max_digits=10, decimal_places=2)
    expiration_date = models.DateTimeField(null=False)
    activation_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Coupon {self.code} with discount {self.discount} until {self.expiration_date}"