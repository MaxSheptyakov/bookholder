from .models import BookType
from django import forms
import boto3
from decouple import config
from django.utils.text import slugify


def get_available_book_types():
    return BookType.objects.all()


def get_extension(url):
     return url.rsplit('.', 1)[1].lower()


def check_book_extension(file_name):
    valid_extensions = ['fb2', 'djvu', 'pdf', 'txt', 'doc']
    extension = get_extension(file_name)
    if extension not in valid_extensions:
        raise forms.ValidationError('The given URL does not match valid book extensions.')
    return file_name


def get_s3_session_client():
    session = boto3.Session(
        aws_access_key_id=config('AWS_SECRET_KEY_ID'),
        aws_secret_access_key=config('AWS_SECRET_ACCESS_KEY'),
        region_name=config('REGION_NAME'),
    )
    s3 = session.client(
        service_name=config('SERVICE_NAME'),
        endpoint_url=config('ENDPOINT_URL'),
    )
    return s3


def get_book_slug(title, author, book_id):
    return slugify(title + author + str(book_id))

def get_base_url():
    return (config('ENDPOINT_URL') if config('ENDPOINT_URL').endswith('/') else config('ENDPOINT_URL') + '/') \
           + config('BUCKET_NAME') + '/'


def upload_book_to_s3(file, title, author, book_id):
    s3 = get_s3_session_client()
    try:
        url_uploaded = get_book_slug(title, author, book_id) + f'.{get_extension(file.name)}'
        print(url_uploaded)
        s3.upload_fileobj(file, config('BUCKET_NAME'), url_uploaded)
        return get_base_url() + url_uploaded
    except:
        raise


def add_book_to_book_type(type_name, book):
    bt = BookType.objects.get_or_create(book_type=type_name)
    if bt[1]:
        bt[0].save()
    book.book_types.add(bt[0])


def save_book(book_form, file=None):
    if file is None:
        raise
    check_book_extension(file.name)
    book = book_form.save(commit=True)
    # try:
    url = upload_book_to_s3(file, book.title, book.author, book.id)
    # except:
    #     book.delete()
    #     return book
    book.url = url
    book.slug = get_book_slug(book.title, book.author, book.id)
    for book_type in book_form['book_type']:
        if book_type.data['selected']:
            add_book_to_book_type(book_type.data['value'], book)
    print('end saving')
    book.save()
    print('Commited')
    return book
