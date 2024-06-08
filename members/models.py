from django.db import models
from django.shortcuts import render
from django.contrib.auth.models import AbstractUser
from django.conf import settings


# Create your models here.
class User(AbstractUser):
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email
        
    
class FriendRequest(models.Model):
    FRIEND_ACCEPTED = 'accepted'
    FRIEND_VARIENTS = 'varients'
    FRIEND_PENDIND = 'pending'

    FRIEND_CHOICES = [
        (FRIEND_ACCEPTED, 'accepted'),
        (FRIEND_VARIENTS, 'varients'),
        (FRIEND_PENDIND, 'pending')
    ]

    from_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sent_requests', on_delete=models.CASCADE)
    to_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='received_requests', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=FRIEND_CHOICES, default=FRIEND_PENDIND)

    class Meta:
        unique_together = ('from_user', 'to_user')
