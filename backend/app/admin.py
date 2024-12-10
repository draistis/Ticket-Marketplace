from django.contrib import admin
from .models import Coupon, Event, Location, Organizer, User


admin.site.register(User)
admin.site.register(Organizer)
admin.site.register(Location)
admin.site.register(Event)
admin.site.register(Coupon)
