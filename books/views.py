from django.shortcuts import render,redirect
from . import forms
from.import models
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from django.views.generic import CreateView
from django.urls import reverse_lazy

@method_decorator(login_required, name='dispatch')
class AddBookCreateView(CreateView):
    model = models.Book
    form_class = forms.BookForm
    template_name = 'add_books.html' 
    success_url = reverse_lazy('Profile') 

    def form_valid(self, form):
        form.instance.author = self.request.user
        print("Form is valid. File: ", self.request.FILES)
        return super().form_valid(form)

    def form_invalid(self, form):
        print("Form is invalid. Errors: ", form.errors)
        return self.render_to_response(self.get_context_data(form=form))


from django.views.generic import UpdateView
@method_decorator(login_required, name='dispatch')
class EditBookUpdateView(UpdateView):
    model = models.Book
    form_class = forms.BookForm
    template_name = 'add_books.html'
    success_url = reverse_lazy('Profile') 
    pk_url_kwarg = 'id'


from django.views.generic import DeleteView
@method_decorator(login_required, name='dispatch')
class BookDeleteView(DeleteView):
    model = models.Book
    template_name = 'delete_books.html'
    success_url = reverse_lazy('Profile')
    pk_url_kwarg = 'id'

from django.views.generic import DetailView

class DetailBookView(DetailView):
    model = models.Book
    pk_url_kwarg = 'id'
    template_name = 'books/book_details.html'

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        book = self.object 
        reviews =book.reviews.all()

        context['reviews'] = reviews

        return context
    
class ReviewBookView(DetailView):
    model = models.Book
    pk_url_kwarg = 'id'
    template_name = 'books/book_reviews.html'
    success_url =  reverse_lazy('books:details_books')
    
    def post(self, request, *args, **kwargs):
        review_form = forms.ReviewForm(data=self.request.POST)
        book = self.get_object()
        if review_form.is_valid():
            new_review = review_form.save(commit=False)
            new_review.book = book
            new_review.save()
            return redirect('books:details_books', id=book.id)
        return self.get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        book = self.object 
        reviews =book.reviews.all()
        review_form = forms.ReviewForm()

        context['reviews'] = reviews
        context['review_form'] = review_form
        return context