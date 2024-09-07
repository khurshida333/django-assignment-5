from django.contrib import admin
from . import models
# Register your models here.

class BookAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('title',)}
    list_display  =  ['title','slug']

class BorrowedBookAdmin(admin.ModelAdmin):
    list_display  =  ['user']

class ReviewAdmin(admin.ModelAdmin):
    list_display = ['name', 'book', 'created_on']
    search_fields = ['name', 'book__title']


admin.site.register(models.Book,BookAdmin)
admin.site.register(models.Review,ReviewAdmin)
admin.site.register(models.BorrowedBook,BorrowedBookAdmin)