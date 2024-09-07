from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.
 
class HomeView(TemplateView):
    template_name = 'core/index.html'


from books.models import Book
from categories.models import Category

def index(request, category_slug=None):
    data = Book.objects.all()


    if category_slug:
        try:
            category = Category.objects.get(slug=category_slug)
            data = Book.objects.filter(category=category)

        except Category.DoesNotExist:

            data = Book.objects.all()

    categories = Category.objects.all()

    return render(request, 'core/index.html', {'data': data, 'category': categories})
