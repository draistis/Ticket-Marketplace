from django.db import models


class User(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    password_hash = models.CharField(max_length=300)
    permissions = ['ADMIN', 'USER', 'ORGANIZER']
    phone_number = models.CharField(max_length=15, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name + ' - ' + self.email + ' - ' + self.permissions

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
        return self.name + ' - ' + self.manager

class Location(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    capacity = models.IntegerField()

    def __str__(self):
        return self.name + ' - ' + self.city + ', ' + self.country

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
        return self.name + ' - ' + self.start_datetime + ' - ' + self.location

class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    valid_for = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user + ' - ' + self.event + ' - ' + self.created_at

class Tickets(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, default=None)
    sector = models.CharField(max_length=50)
    row = models.CharField(max_length=10)
    seat = models.IntegerField()
    available = models.BooleanField(default=True)
    purchased_at = models.DateTimeField(default=None, null=True)

    def __str__(self):
        return self.event + ' - ' + self.owner + ' - ' + self.sector + ' - ' + self.row + ' - ' + self.seat

class ReservationTicket(models.Model):
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE)
    ticket = models.ForeignKey(Tickets, on_delete=models.CASCADE)

    def __str__(self):
        return self.reservation + ' - ' + self.ticket

class Payment(models.Model):
    reservation = models.ForeignKey(Reservation, on_delete=models.RESTRICT)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = ['CREDIT_CARD', 'STRIPE', 'AT_LOCATION']
    payment_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.reservation + ' - ' + self.total + ' - ' + self.payment_date

class Coupon(models.Model):
    code = models.CharField(max_length=50)
    discount = models.DecimalField(max_digits=10, decimal_places=2)
    expiration_date = models.DateTimeField(null=False)
    activation_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.code + ' - ' + self.discount