from django import forms
from .models import Book, BookType
from .services import check_book_extension, save_book


class BookCreateForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ('title', 'author', 'description', )

    file = forms.FileField()
    book_type = forms.MultipleChoiceField(choices=BookType.TYPE_CHOICES)

    # def save(self, commit=True, file=None):
    #     save_book(super(BookCreateForm, self), commit, file)

