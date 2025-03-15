from django.urls import path
from users import views

urlpatterns = [
    # student
    path('login_user/',views.login_user ,name="login_user"),  
    path('reg_user/',views.reg_user ,name="reg_user"),   
    path('studadmin/',views.studadmin ,name="studadmin"), 
    path('stud_logout/',views.stud_logout ,name="stud_logout"), 
    path('studbookIssued/',views.studbookIssued ,name="studbookIssued"), 
    path('studbookretured/',views.studbookretured ,name="studbookretured"), 
    path('stud_forgetpass',views.stud_forgetpass,name="stud_forgetpass"),
    
    # Teacher
    path('Tlogin_user/',views.Tlogin_user ,name="Tlogin_user"), 
    path('reg_Tech/',views.reg_Tech ,name="reg_Tech"), 
    path('Techadmin/',views.Techadmin ,name="Techadmin"), 
    path('Tlogin_user/',views.Tlogin_user ,name="Tlogin_user"), 
    path('Tech_forgetpass',views.Tech_forgetpass,name='Tech_forgetpass'),
    path('Tech_logout',views.Tech_logout,name='Tech_logout'),
    path('TechbookIssued/',views.TechbookIssued,name='TechbookIssued'),
    path('Techbookretured/',views.Techbookretured,name='Techbookretured')
    
]