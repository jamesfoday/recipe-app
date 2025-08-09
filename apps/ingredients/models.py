from django.db import models
from django.urls import reverse

class Ingredient(models.Model):
    name = models.CharField(max_length=255)
    quantity = models.CharField(max_length=100)
    image = models.ImageField(upload_to='ingredients', blank=True, null=True, default='no_picture.jpg')

    def __str__(self):
        return f"{self.quantity} of {self.name}"

    def get_absolute_url(self):
        return reverse('ingredients:detail', kwargs={'pk': self.pk})
