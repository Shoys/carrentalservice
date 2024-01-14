from django.db import models
from django.contrib.auth.models import User
import uuid

class Car(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    make = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    year = models.IntegerField()
    color = models.CharField(max_length=255)

    class Meta:
        db_table = 'cars'

    def __str__(self):
        return f"{self.make} {self.model} ({self.year})"

class Booking(models.Model):
    STATUS_CHOICES = [
        ('confirmed', 'Confirmed'),
        ('in-progress', 'In-progress'),
        ('completed', 'Completed'),
    ]

    bookingId = models.CharField(max_length=36, primary_key=True, default=uuid.uuid4)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    startTime = models.DateTimeField()
    endTime = models.DateTimeField()
    status = models.CharField(max_length=15, choices=STATUS_CHOICES)

    class Meta:
        db_table = 'booking'

    def __str__(self):
        return f"Booking {self.bookingId} for {self.car}"
