from django.db import models

class WaitingPatient(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    checkin_time = models.DateTimeField(auto_now_add=True)

