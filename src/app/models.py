from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    pass

class Resume(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    file = models.FileField(upload_to='app/')  # uploaded files go into MEDIA_ROOT/resumes/

    def __str__(self):
        return f"{self.name} - {self.email}"