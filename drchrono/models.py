from django.db import models

class Patient(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)
    first_name = models.CharField(max_length=255)
    middle_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
