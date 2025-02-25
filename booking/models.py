from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Room(models.Model):
    ROOM_TYPES = [
        ('Single', 'Single'),
        ('Double', 'Double'),
        ('Suite', 'Suite'),
    ]
    
    room_number = models.CharField(max_length=10, unique=True)
    room_type = models.CharField(max_length=10, choices=ROOM_TYPES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    is_available = models.BooleanField(default=True)
    
    # Added Models
    room_name = models.CharField(max_length=255)
    
    def __str__(self):
        return f"{self.room_name} - {self.room_type}"


class Booking(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    guest_name = models.CharField(max_length=100)
    guest_email = models.EmailField()
    check_in = models.DateField()
    check_out = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Added Models
    total_guest = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    special_request = models.CharField(max_length=200)
    
    def __str__(self):
        return f"Booking for {self.guest_name} ({self.room.room_number})"
