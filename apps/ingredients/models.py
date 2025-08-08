from django.db import models

class Ingredient(models.Model):
    name = models.CharField(max_length=255)
    quantity = models.CharField(max_length=100)  # e.g., '2 cups', '500g'

    def __str__(self):
        return f"{self.quantity} of {self.name}"
