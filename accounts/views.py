from django.shortcuts import render ,redirect
from django.views.generic import FormView, TemplateView, ListView
from .forms import UserRegistrationForm
from django.urls import reverse_lazy

from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView,LogoutView

from django.http import HttpResponseRedirect
from django.views import View

from .forms import UserUpdateForm
from books.models import BorrowedBook, Book

# Create your views here.

class UserRegistrationView(FormView):
    template_name ='accounts/user_registration.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('register')

    def form_valid(self,form):
        user = form.save()  
        login(self.request, user)
        return super().form_valid(form) 

class UserLoginView(LoginView):
    template_name = 'accounts/user_login.html'
    def get_success_url(self):
           return reverse_lazy('home')

class UserLogoutView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
           logout(request)
        return HttpResponseRedirect(reverse_lazy('home'))
    
class UserBankAccountUpdateView(View):
    template_name = 'accounts/update_profile.html'

    def get(self, request):
        form = UserUpdateForm(instance=request.user)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = UserUpdateForm(request.POST, instance=request.user) 
        if form.is_valid():
            form.save()
            return redirect('profile') 
        return render(request, self.template_name, {'form': form})
    
class ProfilePageView(TemplateView):
    template_name = 'accounts/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        borrowed_books = BorrowedBook.objects.filter(user=self.request.user)
        context['borrowed_books'] = borrowed_books
        print(f"Context borrowed_books: {borrowed_books}") 
        return context