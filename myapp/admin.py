from django.contrib import admin
from .models import post,Author,Book,Category,MyUser,IssuedBookRecord


# Register your models here.
@admin.register(post)
class postAdmin(admin.ModelAdmin):
    list_display=['id','title','email','password']
    
admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Book)
admin.site.register(MyUser)
admin.site.register(IssuedBookRecord)
    