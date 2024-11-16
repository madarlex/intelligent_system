# Generated migration file in your_app_name/migrations/xxxx_load_data.py
from django.db import migrations
import json
from pathlib import Path
from datetime import datetime


def reverse_load_data(apps, schema_editor):
    Book = apps.get_model("books", "Book")
    Genre = apps.get_model("books", "Genre")

    # Delete all books and genres created by this migration
    Book.objects.all().delete()
    Genre.objects.all().delete()


def load_data(apps, schema_editor):
    # Get the Genre and Book models
    Genre = apps.get_model("books", "Genre")
    Book = apps.get_model("books", "Book")

    # Load genres from genres.json and create Genre entries
    genres_file_path = Path(__file__).resolve().parent.parent.parent / "genres.json"
    with open(genres_file_path, "r") as f:
        genres = json.load(f)
        genre_map = {}  # Dictionary to map genre names to Genre objects
        for genre_name in genres:
            genre_obj, created = Genre.objects.get_or_create(name=genre_name)
            genre_map[genre_name] = genre_obj

    # Load books from books_data.json and create Book entries
    books_file_path = (
        Path(__file__).resolve().parent.parent.parent
        / "books_data_with_recommendations.json"
    )
    with open(books_file_path, "r") as f:
        books = json.load(f)
        book_objects = {}  # Temporary dictionary to hold book objects by title

        for book_data in books:
            # Convert publish_date to datetime if it exists
            publish_date = None
            if book_data["publish_date"]:
                try:
                    publish_date = datetime.fromisoformat(book_data["publish_date"])
                except ValueError:
                    publish_date = None

            # Create Book object without recommended_books to avoid circular dependency
            book_obj = Book.objects.create(
                title_complete=book_data["title_complete"],
                description=book_data["description"],
                image_url=book_data["image_url"],
                publisher=book_data["publisher"],
                authors=book_data["authors"],
                publish_date=publish_date,
                num_pages=book_data["num_pages"],
                isbn=book_data["isbn"],
                isbn13=book_data["isbn13"],
                genres_vector=book_data["genres_vector"],
                price=book_data["price"],
            )

            # Add genres to the Book object
            for genre_name in book_data["genres"]:
                if genre_name in genre_map:
                    book_obj.genres.add(genre_map[genre_name])

            # Save the object in a dictionary for later reference
            book_objects[book_obj.title_complete] = book_obj

    # Second pass to update the recommended_books field for each book
    for book_data in books:
        book_obj = book_objects.get(book_data["title_complete"])
        if book_obj and "recommended_books" in book_data:
            recommended_ids = [
                book_objects[title].id
                for title in book_data["recommended_books"]
                if title in book_objects
            ]
            book_obj.recommended_books = recommended_ids
            book_obj.save()


class Migration(migrations.Migration):
    dependencies = [
        (
            "books",
            "0001_initial",
        ),  # replace with the last migration name
    ]

    operations = [
        migrations.RunPython(load_data, reverse_code=reverse_load_data),
    ]
