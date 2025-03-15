from django.urls import path
from book import views

urlpatterns = [
    
    path('booksIssued/',views.booksIssued ,name="booksIssued"),
    path('returnbook/',views.returnbook ,name="returnbook"),
    path('manage_fine/',views.manage_fine ,name="manage_fine"),
    path('Pay_fine/', views.Pay_fine,name="Pay_fine"),
    
]