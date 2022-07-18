from django import forms

from books.models import Book, Comment

import datetime


class DateInput(forms.DateInput):
    input_type = 'date'


class BookForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super(BookForm, self).__init__(*args, **kwargs)

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Book
        fields = ('name', 'author_id', 'price', 'founded_on', 'file', 'front_pic', 'book_desc')
        widgets = {
            'founded_on': DateInput(),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'rating', 'body')

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs = {'placeholder': 'Enter name', 'class': 'form-control'}
        self.fields['email'].widget.attrs = {'placeholder': 'Enter email', 'class': 'form-control'}
        self.fields['rating'].widget.attrs = {'class': 'form-control'}
        self.fields['body'].widget.attrs = {'placeholder': 'Comment here...', 'class': 'form-control', 'rows': '5'}
