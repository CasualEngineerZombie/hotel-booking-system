from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid


class Amenity(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
    
    
class Room(models.Model):
    ROOM_TYPES = [
        ('Single', 'Single'),
        ('Double', 'Double'),
        ('Suite', 'Suite'),
    ]
    photo = models.ImageField(upload_to='rooms/')
    room_number = models.CharField(max_length=10, unique=True)
    room_type = models.CharField(max_length=10, choices=ROOM_TYPES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    is_available = models.BooleanField(default=True)
    
    # UUID for unique identification (but not used as the primary key)
    max_guest = models.IntegerField()
    area = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        help_text="Room area in square meters"
    )
    room_uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    room_name = models.CharField(max_length=255)
    
    # Many-to-many relationship with Amenity
    amenities = models.ManyToManyField(Amenity, related_name='rooms', blank=True)
    
    def __str__(self):
        return f"{self.room_name} - {self.room_type}"


class Booking(models.Model):
    # The foreign key will reference Room's default primary key (id)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    guest_name = models.CharField(max_length=100)
    guest_email = models.EmailField()
    check_in = models.DateField()
    check_out = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    # UUID for unique identification (but not used as the primary key)
    booking_uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    total_guest = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    special_request = models.CharField(max_length=200)
    paid = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Booking for {self.guest_name} ({self.room.room_number})"
