from django.shortcuts import render

# Create your views here.
from .models import Book, Author, BookInstance, Genre
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.decorators.clickjacking import xframe_options_sameorigin
from django.views.decorators.clickjacking import xframe_options_deny
from django.shortcuts import render,redirect,HttpResponse
from django.urls import reverse_lazy 
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.forms import PasswordChangeForm
from catalog.forms import EigenePasswortchangeForm

from django.contrib.auth import logout,login,authenticate

from django.contrib import messages


class PasswordsChangeView(PasswordChangeView):
     form_class=PasswordChangeForm
     #form_class=PasswordChangeForm
  #   success_url = reverse_lazy('index')
     success_url = reverse_lazy('password_change_success')
     template_name = 'registration/password_change.html'

#def login_user(request):
#     if request.method=="POST":
#         username=request.POST['username']
#         password=request.POST['password']
#         user=authenticate(request,username,password)
#         if user is not None:
#              login(request,user)
#              return redirect('index')
#         else:
#              messages.success(request,"Login fehlgeschlagen")
#              return redirect('index')        
        
     
     
def logout_user(request):
     logout(request)
     messages.success(request,"Sie sind jetzt ausgeloggt")
     return redirect("index")
               

"""
def  EigenePasswortchangeView(request):
  
    seite = 'reg'
    form = EigenePasswortchangeForm

    if request.method == 'POST':
        form = EigenePasswortchangeForm(request.POST)
        if form.is_valid():
            form.save()
          
            return reverse_lazy('registration/password_success.html')
        else:
            messages.error(request, "Fehlerhafte Eingabe!")

    ctx = {'form': form, 'seite': seite}
    return render(request, 'registration/password_change.html', ctx)
"""

     

def password_change_success(request):
     return render(request,'registration/password_change_success.html',{})

@xframe_options_sameorigin
def index(request):
    """View function for home page of site."""

    # user = User.objects.create_user(email="ll55@gmail.com",password="uU123456",username="le5")
    # user.set_password("uU123456")
    # user.save()
    
    bindrin = 'ohne'

    if  request.user.is_authenticated:
         passwordneu='4321234$'
         user1 = request.user.username
         user_instance= User.objects.filter(username=user1).count()
         user=User.objects.filter(username=user1)
         bindrin =  "mit" + user1 + " " + str(user_instance)
     #    user.set_password("uU123456")
     #    user.save()
         
         request.user.set_password(passwordneu)
         request.user.save
        # print (passwordneu)
        #bindrin = 'mit'

    # Generate counts of some of the main objects
    
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    num_visits = request.session.get('num_visits', 0)
    num_visits += 1
    request.session['num_visits'] = num_visits

    # The 'all()' is implied by default.
    num_authors = Author.objects.count()

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_visits': num_visits,
        'bindrin': bindrin,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)


from django.views import generic


class BookListView(LoginRequiredMixin,generic.ListView):

      model = Book
      context_object_name = 'book_list' 

class BookDetailView(generic.DetailView):
      model = Book

class AuthorListView(generic.ListView):
      model = Author
      context_object_name = 'author_list' 

class AuthorDetailView(generic.DetailView):
      model = Author


from django.contrib.auth.mixins import LoginRequiredMixin

class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return (
            BookInstance.objects.filter(borrower=self.request.user)
            .filter(status__exact='o')
            .order_by('due_back')
        )

# alle ausgeliehenen Bücher

class AllBorrowedBooksListView(LoginRequiredMixin,generic.ListView):
  
    """Generic class-based view listing books on loan all."""
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed.html'
    paginate_by = 10

    def get_queryset(self):
        return (
            BookInstance.objects.filter(status__exact='o')
            .order_by('due_back')
        )
    


import datetime

from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse

from catalog.forms import RenewBookForm

@login_required
@permission_required('catalog.can_mark_returned', raise_exception=True)

def renewbooklibrarian(request, pk):


    """View function for renewing a specific BookInstance by librarian."""
    book_instance = get_object_or_404(BookInstance, pk=pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = RenewBookForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            book_instance.due_back = form.cleaned_data['renewal_date']
    
            book_instance.save()

            # redirect to a new URL:    
            
            return HttpResponseRedirect(reverse('bookdetail', args=[str(book_instance.book_id)]))

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})

    context = {
        'form': form,
        'book_instance': book_instance,
    }

    return render(request, 'catalog/book_renew_librarian.html', context)



     