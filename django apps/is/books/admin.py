from django.db import transaction
import pickle
from sklearn.neighbors import NearestNeighbors
import numpy as np
from django.contrib import admin
from .models import Book, Genre


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    # Display fields in the list view
    list_display = (
        "id",
        "title_complete",
        "publisher",
        "publish_date",
        "authors",
        "display_genres",
    )
    # Add search functionality
    search_fields = ("title_complete", "authors", "publisher", "genres__name")
    # Enable filtering by genres and publish date
    list_filter = ("genres",)
    # Enable editable fields directly in the list view
    list_editable = (
        "title_complete",
        "publisher",
        "publish_date",
        "authors",
    )
    # Set the fields to display in the detail view
    fields = (
        "title_complete",
        "description",
        "image_url",
        "publisher",
        "authors",
        "genres",
        "price",
        "publish_date",
        "num_pages",
        "isbn",
        "isbn13",
        "recommended_books",
    )
    # Enable inline editing for many-to-many relationships
    filter_horizontal = ("genres",)
    # Order by title by default
    ordering = ("id",)

    # Custom method to display genres as a comma-separated list
    def display_genres(self, obj):
        return ", ".join([genre.name for genre in obj.genres.all()])

    display_genres.short_description = "Genres"

    def save_model(self, request, obj, form, change):
        # Load the MultiLabelBinarizer
        with open("./data/mlb_genres.pkl", "rb") as f:
            mlb = pickle.load(f)

        if not change:
            # Custom title logic to capitalize each word
            obj.title_complete = obj.title_complete.title()

            # Default publisher if not set
            if not obj.publisher:
                obj.publisher = "Default Publisher"

            # Save the model instance in a single transaction to ensure atomicity
            with transaction.atomic():
                super().save_model(
                    request, obj, form, change
                )  # Save obj to get ID for KNN

                # Retrieve genre names from the newly created object and vectorize them
                genre_names = [genre.name for genre in obj.genres.all()]
                obj.genres_vector = mlb.transform([genre_names])[0].tolist()

                # Retrieve only `genres_vector` and `id` for all books except the current one
                all_books = Book.objects.exclude(id=obj.id).values_list(
                    "genres_vector", "id"
                )
                genres_vectors = [
                    book[0] for book in all_books
                ]  # List of genre vectors
                book_ids = [book[1] for book in all_books]  # List of book IDs

                # Fit KNN model on all genre vectors
                knn = NearestNeighbors(n_neighbors=16, metric="cosine")
                knn.fit(genres_vectors)

                # Get the nearest neighbors for the current book
                _, indices = knn.kneighbors([obj.genres_vector], n_neighbors=16)
                recommended_ids = [
                    book_ids[i] for i in indices[0] if book_ids[i] != obj.id
                ][:15]

                # Assign recommended book IDs to the recommended_books field
                obj.recommended_books = recommended_ids
        obj.save()  # Save again with updated fields
