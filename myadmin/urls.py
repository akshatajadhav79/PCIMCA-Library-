from django.urls import path
from myadmin import views

urlpatterns = [
    
    # Admin
    
    path('adminpanel/',views.adminpanel ,name="adminpanel"), 
    path('addauthor/',views.addauthor ,name="addauthor"), 
    path('addcat/',views.addcat ,name="addcat"), 
    path('addbook/',views.addbook ,name="addbook"), 
    path('viewbooks/',views.viewbooks ,name="viewbooks"), 
    
    path('admin_login/',views.admin_login ,name="admin_login"),
    path('admin_logout/',views.admin_logout ,name="admin_logout"), 
    path('admin_forgetpass/',views.admin_forgetpass,name="admin_forgetpass"),
    
    path('studManage/', views.studManage,name='studManage'),
    path('TechManage/', views.TechManage,name='TechManage'),
    
]