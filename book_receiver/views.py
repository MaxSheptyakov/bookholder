from django.shortcuts import render, redirect, get_object_or_404
from .models import BookType, Book
from .services import get_available_book_types, save_book
from .forms import BookCreateForm
from django.contrib import messages


def main(request):
    return render(request, 'book_receiver/main.html')


def catalog(request):
    book_types = get_available_book_types()
    return render(request, 'book_receiver/catalog.html', {'book_types': book_types})


def upload_book(request):
    if request.method == 'POST':
        # Форма отправлена.
        form = BookCreateForm(request.POST, request.FILES)
        if form.is_valid():
            print(1)
            # Данные формы валидны.
            cd = form.cleaned_data
            save_book(form, request.FILES['file'])
            #new_item = form.save(commit=True, file=request.FILES['file'])
            messages.success(request, 'Image added successfully')
            # Перенаправляем пользователя на страницу сохраненного изображения.
            return redirect('book_receiver:catalog')
    else:
        # Заполняем форму данными из GET-запроса.
        form = BookCreateForm(request.GET, request.FILES)
    return render(request, 'book_receiver/upload_book.html',
                  {'form': form})


def book_info(request, book_slug):
    book = get_object_or_404(Book, slug=book_slug)
    return render(request, 'book_receiver/book_info.html', {'book': book})


def donations(request):
    return render(request, 'book_receiver/donations.html')