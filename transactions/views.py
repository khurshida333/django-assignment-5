from django.shortcuts import render ,get_object_or_404, redirect
from django.utils.timezone import now 
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, TemplateView
from django.views.generic import CreateView, ListView
from django.views import View

from django.urls import reverse_lazy
from datetime import datetime
from django.contrib import messages
from django.db.models import Sum
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template.loader import render_to_string

from .models import Transaction,UserBankAccount
from books.models import Book, BorrowedBook
from accounts.models import UserBankAccount
from transactions.models import Transaction
from .forms import (
    DepositForm,
)
from transactions.constants import DEPOSIT,WITHDRAWAL



def send_transaction_email(user, amount, subject, template):
   
    user_profile = UserBankAccount.objects.get(user=user)
    balance = user_profile.balance

    
    context = {
        'user': user,
        'amount': amount,
        'balance': balance,
    }

   
    html_message = render_to_string(template, context)
    plain_message = strip_tags(html_message)  

    
    email = EmailMultiAlternatives(
        subject,
        plain_message,
        'akhurshida70@gmail.com',  
        [user.email],
    )
    email.attach_alternative(html_message, "text/html")
    
    email.send()

def send_borrow_return_email(user, amount, book_id, subject, template):

   
    print(f"Sending return email to {user.email} for book ID {book_id}.")


    user_profile = UserBankAccount.objects.get(user=user)
    balance = user_profile.balance

   
    try:
        borrowed_book = BorrowedBook.objects.get(book__id=book_id)
        book = borrowed_book.book

    except BorrowedBook.DoesNotExist:
        print("Book not found.")
        return

   
    context = {
        'user': user,
        'amount': amount,
        'balance': balance,
        'book': book.title
    }

   
    html_message = render_to_string(template, context)
    plain_message = strip_tags(html_message) 

   
    email = EmailMultiAlternatives(
        subject,
        plain_message,
        'akhurshida70@gmail.com', 
        [user.email],
    )
    email.attach_alternative(html_message, "text/html")
    
    
    print(f"Email subject: {subject}, recipient: {user.email}")

    try:
        email.send()
        print("email sent successfully.")
    except Exception as e:
        print(f"Error sending email: {e}")


class TransactionCreateMixin(LoginRequiredMixin, CreateView):
    template_name = 'transactions/transaction_form.html'
    model = Transaction
    title = ''
    success_url = reverse_lazy('transactions:transaction_report')
    
    
    def get_form_kwargs(self): 
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'account': self.request.user.account
        })
        return kwargs


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 
        context.update({
            'title': self.title
        })

        return context
    
class DepositMoneyView(TransactionCreateMixin):
    form_class = DepositForm
    title = 'Deposite'

    def get_initial(self):
        initial = {'transaction_type': DEPOSIT}
        return initial

    def form_valid(self, form):
        amount = form.cleaned_data.get('amount') 
        account = self.request.user.account
        account.balance += amount 
        account.save(
            update_fields=[
                'balance'
            ]
        )
        messages.success(
            self.request,
            f'{"{:,.2f}".format(float(amount))}$ was deposited to your account successfully'
        )

        send_transaction_email(self.request.user,amount, "Deposite Message", "transactions/deposite_email.html")
    
        return super().form_valid(form)
@login_required 
def BorrowBook(request, id):
   
    book = get_object_or_404(Book, pk=id)
    user_profile = get_object_or_404(UserBankAccount, user=request.user)

    
    if book.is_borrowed:
        messages.error(request, "This book is already borrowed by someone else.")
        return redirect('books:details_books', id=id)

    if user_profile.balance < book.borrowing_price:
        messages.error(request, "Insufficient balance to borrow the book.")
        return redirect('books:details_books', id=id)

    
    user_profile.balance -= book.borrowing_price
    user_profile.save()

    
    balance_after_transaction = user_profile.balance

    Transaction.objects.create(
        account=user_profile,
        amount=-book.borrowing_price,
        transaction_type=WITHDRAWAL,
        timestamp=datetime.now(),
        balance_after_transaction=balance_after_transaction,
    )

    
    book.is_borrowed = True
    book.save()
    book.borrower.add(request.user)  
    
    
    borrowed_book = BorrowedBook.objects.create(
        user=request.user,
        book=book,
        borrowed_date=datetime.now()
    )

    
    send_borrow_return_email(request.user, book.borrowing_price, book.id, "Borrow Message", "transactions/borrow_email.html")

    
    messages.success(request, "Book borrowed successfully!")
    return redirect('books:details_books', id=id)

@login_required
def ReturnBook(request, id):
    
    book = get_object_or_404(Book, pk=id)
    user_profile = get_object_or_404(UserBankAccount, user=request.user)

    if book.is_borrowed:
        user_profile.balance += book.borrowing_price
        user_profile.save()
       
        
        borrowed_books = BorrowedBook.objects.filter(user=request.user, book=book)
        if borrowed_books.exists():
          
            send_borrow_return_email(request.user, book.borrowing_price, book.id, "Return Message","transactions/return_email.html")
            borrowed_books.delete()
            

       
        balance_after_transaction = user_profile.balance

       
        Transaction.objects.create(
            account=user_profile,
            amount=book.borrowing_price,
            transaction_type=DEPOSIT,
            timestamp=now(),
            balance_after_transaction=balance_after_transaction,
        )

        book.is_borrowed = False
        book.save()
            

        
        messages.success(request, "Book returned successfully!")
        return redirect('transactions:borrow_report')
    else:
        
        messages.warning(request, "This book was not borrowed.")
        return redirect('transactions:borrow_report')
         
class TransactionReportView(LoginRequiredMixin, ListView): 
    template_name = 'transactions/transaction_report.html'
    model = Transaction
    balance = 0 
    context_object_name = 'report_list'
    
    def get_queryset(self):
        queryset = super().get_queryset().filter( account=self.request.user.account)

        start_date_str = self.request.GET.get('start_date')  
        end_date_str = self.request.GET.get('end_date')
        
        if start_date_str and end_date_str:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
            
            queryset = queryset.filter(timestamp__date__gte=start_date, timestamp__date__lte=end_date)
            self.balance = Transaction.objects.filter(
                timestamp__date__gte=start_date, timestamp__date__lte=end_date
            ).aggregate(Sum('amount'))['amount__sum']
        else:
            self.balance = self.request.user.account.balance
       
        return queryset.distinct() 
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'account': self.request.user.account
        })
  
        return context
class BorrowReportView(LoginRequiredMixin, ListView): 
    template_name = 'transactions/borrow_report.html'
    model = BorrowedBook
    context_object_name = 'borrow_report_list'
    
    def get_queryset(self):
        queryset = super().get_queryset().filter( user=self.request.user)
        queryset = queryset.order_by('-borrowed_date')
        

        self.balance = UserBankAccount.objects.get(user=self.request.user).balance
       
        return queryset.distinct() 
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'account': self.request.user,
            'balance': self.balance,
        })
  
        return context
    


