from django.db import models

class endgame(models.Model):
    location = models.CharField(max_length=100)
    disasterTp = models.CharField(max_length=100)
    disasterDt = models.CharField(max_length=1000)

    def __str__(self):
        return f"{self.location} {self.disasterTp} {self.isasterDt}"
