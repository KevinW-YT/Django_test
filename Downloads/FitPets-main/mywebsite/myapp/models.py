from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class ToDoItem(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    completed = models.BooleanField(default=False)
    category = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)  # Link task to a user

    EXERCISE = 'Exercise'
    STRETCHING = 'Stretching'
    CARDIO = 'Cardio'

    CATEGORY_CHOICES = [
        (EXERCISE, 'Exercise'),
        (STRETCHING, 'Stretching'),
        (CARDIO, 'Cardio'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=11, choices=CATEGORY_CHOICES)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    

class Pet(models.Model):
    name = models.CharField(max_length=100)
    price = models.PositiveIntegerField()  # Cost of the pet in coins
    image = models.CharField(max_length=255)  # Store the static file path as a string

    def __str__(self):
        return self.name

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    points = models.PositiveIntegerField(default=0)  # User's coin balance
    pets = models.ManyToManyField(Pet, blank=True)  # Pets owned by the user
    current_pet = models.ForeignKey(Pet, on_delete=models.SET_NULL, null=True, blank=True, related_name='current_pet')
    
    def __str__(self):
        return f"{self.user.username}'s Profile"