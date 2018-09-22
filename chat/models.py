import os

from django.contrib.auth.models import User
from django.db import models


class Room(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField()


class Message(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    room = models.ForeignKey('Room', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=128)
