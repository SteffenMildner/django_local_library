from django.contrib import admin

# Register your models here.
from .models import Author, Genre, Book, BookInstance,PropertyBookInstance

# admin.site.register(Book)
#admin.site.register(Author)
admin.site.register(Genre)
#admin.site.register(PropertyBookInstance)

#admin.site.register(BookInstance)
# admin.site.register(Language)

# Define the admin class

class BooksInline(admin.TabularInline):
   model = Book

@admin.register(Author)

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'date_of_birth')
  
    inlines = [BooksInline]

#class AuthorAdmin(admin.ModelAdmin):
#    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')

#    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]

# Register the Admin classes for Book using the decorator

@admin.register(PropertyBookInstance)

class PropertyBookInstanceAdmin(admin.ModelAdmin):
   list_display = ('wert','fileofproperty')
  
    

class BooksInstanceInline(admin.TabularInline):
   model = BookInstance

class PropertyBookInstanceInline(admin.TabularInline):
   model = PropertyBookInstance

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')
  
    inlines = [BooksInstanceInline]
 
  


# Register the Admin classes for BookInstance using the decorator
@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
        inlines = [PropertyBookInstanceInline]
         
        list_filter = ('status', 'due_back')
        list_display = ('id', 'imprint', 'book')
        list_display = ('book', 'status', 'borrower', 'due_back', 'id')
        list_filter = ('status', 'due_back')

        fieldsets = (
           (None, {
            'fields': ('book', 'imprint', 'id')
           }),
             ('Availability', {
            'fields': ('status', 'due_back', 'borrower')
        }),
       )
        
   

# Register the admin class with the associated model
#admin.site.register(Author, AuthorAdmin)



#admin.site.register(Book, AuthorAdmin)
#admin.site.register(BookInstance, AuthorAdmin)