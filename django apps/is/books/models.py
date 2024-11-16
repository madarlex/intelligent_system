from django.db import models
from django.contrib.postgres.fields import ArrayField


# Create your models here.
class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    title_complete = models.CharField(max_length=255)
    description = models.TextField()
    image_url = models.URLField(max_length=500, null=True, blank=True)
    publisher = models.CharField(max_length=100)
    authors = models.CharField(max_length=255)
    genres = models.ManyToManyField("Genre", related_name="books")
    publish_date = models.DateTimeField(null=True, blank=True)
    num_pages = models.IntegerField(null=True, blank=True)
    isbn = models.CharField(max_length=10, null=True, blank=True)
    isbn13 = models.CharField(max_length=13, null=True, blank=True)
    genres_vector = ArrayField(models.IntegerField(), blank=True, default=list)
    recommended_books = ArrayField(models.IntegerField(), blank=True, default=list)
    price = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.title_complete
