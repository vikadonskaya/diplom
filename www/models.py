from django.contrib.contenttypes.fields import GenericRelation
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from star_ratings.models import Rating

from authreg.models import CustomUser


class Category(models.Model):
    name = models.CharField(null=True, blank=True)

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=100)
    category = models.ManyToManyField(Category)

    def __str__(self):
        return self.name

class Product(models.Model):
    photo = models.FileField(upload_to='image')
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.IntegerField()
    quantity = models.IntegerField()
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, null=True, blank=True)  # Связь с моделью Brand
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)


    def __str__(self):
        return self.name

class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    text = models.TextField()
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        default=5
    )
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.user.username