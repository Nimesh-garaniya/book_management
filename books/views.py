from books.ajax.ajax import AjaxDatatableView
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView

from books.forms import BookForm, CommentForm
from books.models import Book

from accounts.views import LoginRequiredMixin


class BookList(ListView, LoginRequiredMixin):
    model = Book
    template_name = "BookList.html"
    context_object_name = "data"
    paginate_by = 5
    queryset = Book.objects.all()


class BookAjaxDatatableView(AjaxDatatableView, LoginRequiredMixin):
    model = Book
    initial_order = [[1, "asc"]]
    length_menu = [[5, 25, 100, -1], [5, 10, 15, 'all']]
    search_values_separator = '+'

    column_defs = [
        {'name': 'name', 'visible': True, 'searchable': True, },
        {'name': 'author_id', 'foreign_field': 'author_id__name', 'visible': True, 'searchable': True, },
        {'name': 'price', 'visible': True, 'searchable': True, },
        {'name': 'founded_on', 'visible': True, 'searchable': True, },
        {'name': 'file', 'visible': True, 'orderable': False, 'searchable': False, },
        {'name': 'front_pic', 'visible': True, 'orderable': False, 'searchable': False, },
        {'name': 'book_desc', 'visible': True, 'orderable': False, 'searchable': True, },
        {'name': 'edit_book', 'title': 'Edit Book', 'placeholder': True, 'searchable': False, 'orderable': False, },
        {'name': 'View_book', 'title': 'View Book', 'placeholder': True, 'searchable': False, 'orderable': False, },

    ]

    def customize_row(self, row, obj):
        row['name'] = f"""<p style="white-space: break-spaces; width:100px">{obj.name}</p>"""
        row['author_id'] = f"""<p style="white-space: break-spaces;">{obj.author_id}</p>"""
        row['price'] = f"""<p style="white-space: break-spaces;">{obj.price}</p>"""
        row['founded_on'] = f"""<p style="white-space: break-spaces;">{obj.founded_on}</p>"""
        row['file'] = f"""<a class='btn btn-primary' href="{obj.file.url}" target="_blank" style="white-space: break-spaces;">View</a>"""
        row['front_pic'] = f"""<img class='photo' src='{obj.front_pic.url}' style="width: 100px; height: 150px; white-space: break-spaces;">"""
        row['book_desc'] = f"""<p style="white-space: break-spaces;">{obj.book_desc}</p>"""
        edit_book = reverse_lazy('book:BookUpdate', kwargs={'pk': obj.pk})
        view_book = reverse_lazy('book:BookDetail', kwargs={'pk': obj.pk})
        row['edit_book'] = f"""<a href='{edit_book}' class='btn btn-danger'>Edit</a>"""
        row['View_book'] = f"""<a href='{view_book}' class='btn btn-success'>View</a>"""
        return


class BookCreate(CreateView, LoginRequiredMixin):
    model = Book
    form_class = BookForm
    template_name = "CreateView.html"
    success_url = reverse_lazy('book:BookList')

    def get_context_data(self, **kwargs):
        ctx = super(BookCreate, self).get_context_data(**kwargs)
        ctx['title'] = "Add Book"
        ctx['header'] = "Add Book"
        return ctx


class BookUpdate(UpdateView, LoginRequiredMixin):
    model = Book
    form_class = BookForm
    template_name = "UpdateView.html"
    success_url = reverse_lazy('book:BookList')

    def get_context_data(self, **kwargs):
        ctx = super(BookUpdate, self).get_context_data(**kwargs)
        ctx['title'] = "Book Update"
        ctx['header'] = "Book Update"
        return ctx


class BookDetail(View):
    model = Book
    template_name = "BookDetail.html"
    form_class = CommentForm

    def get(self, request, pk):
        book = Book.objects.get(pk=pk)
        form = CommentForm()
        context = {'book': book, 'form': form}
        return render(request, 'BookDetail.html', context)

    def post(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        if request.method == 'POST':
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.book = book
                comment.save()
                return redirect('book:BookDetail', pk=pk)
        else:
            form = CommentForm()
        template = 'BookDetail.html'
        context = {'form': form}
        return render(request, template, context)
