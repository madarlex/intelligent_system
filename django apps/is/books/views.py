from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import Genre, Book
from django.core.paginator import Paginator
from django.db.models import Q


# Create your views here.
def home(request):
    return render(request, "books/index.html")


def subpage(request, book_id):
    genre_id = request.GET.get("genre")
    # Retrieve the book object with the given book_id or return 404 if not found
    book = get_object_or_404(Book, id=book_id)
    recommend_range = range(1, 16)
    # Pass the book to the template context
    # Get the number of recommended books from the query parameter, default to 5
    number_of_recommended = int(request.GET.get("number_of_recommended", 5))
    recommended_books = Book.objects.filter(id__in=book.recommended_books)[
        :number_of_recommended
    ]
    genres = Genre.objects.all()
    context = {
        "book": book,
        "recommend_range": recommend_range,
        "number_of_recommended": number_of_recommended,
        "recommended_books": recommended_books,
        "selected_genre": int(genre_id) if genre_id else 0,
        "genres": genres,
    }
    return render(request, "books/subpage.html", context)


# View to display all genres in the sidebar
def genre_list(request):
    genres = Genre.objects.all()
    return render(request, "books/index.html", {"genres": genres})


# View to display books based on selected genre
def books_by_genre(request, genre_id):
    genre = get_object_or_404(Genre, id=genre_id)
    books = Book.objects.filter(genres=genre)
    return render(request, "books/index.html", {"books": books, "genre": genre})


def book_list(request):
    genre_id = request.GET.get("genre")  # Get genre filter from query parameters
    page_number = request.GET.get("page")  # Get page number from query parameters
    search_query = request.GET.get("search")  # Get search query from query parameters
    # Apply strip() only if search_query is not None
    if search_query:
        search_query = search_query.strip()
    # Filter books by genre if a genre is selected
    if genre_id and genre_id != "0":
        selected_genre = get_object_or_404(Genre, id=genre_id)
        books = Book.objects.filter(genres=selected_genre)
    elif search_query:
        books = Book.objects.filter(
            Q(title_complete__icontains=search_query)
            | Q(authors__icontains=search_query)
        )
    else:
        books = Book.objects.all()

    genres = Genre.objects.all()
    # Set up pagination (e.g., 5 books per page)
    paginator = Paginator(books, 20)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
        "selected_genre": int(genre_id) if genre_id else 0,
        "genres": genres,  # Pass all genres if needed for filtering in the template
    }

    return render(request, "books/index.html", context)
