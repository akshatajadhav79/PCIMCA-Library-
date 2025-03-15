from django.shortcuts import render,HttpResponseRedirect,redirect
from django.contrib import messages
from myapp.models import Book, IssuedBookRecord, MyUser
from django.http import JsonResponse



# Create your views here.
# Student
def login_user(request):
    if request.method == "POST":
        username1=request.POST.get('username')
        password1= request.POST.get('password')
    
        if not MyUser.objects.filter(email=username1).exists():
            messages.error(request,"Invalid email ")
            return redirect('/users/login_user') 
        
        usern = MyUser.objects.filter(email=username1).exists()
        if usern == True:
            user=MyUser.objects.get(email=username1)
            if user.password == password1:
                request.session['user_id'] = user.pk
                request.session['user_email'] = user.email
                request.session['user_profile'] = user.CATEGORY_CHOICES
                messages.error(request,"Thank you for login.")
                return redirect(f"/users/studadmin")
            else:
                messages.error(request,"Wronge Password.")

    return render(request,"student/login.html")

def reg_user(request):
    if request.method == "POST":
        username = request.POST.get('username')
        full_name = request.POST.get('fullname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        cpassword = request.POST.get('cpassword')

        # Check if username already exists
        if MyUser.objects.filter(username=username).exists():
            messages.error(request,'Email is Already taken')
            return HttpResponseRedirect(request.path_info)

        # Check if passwords match
        if password != cpassword:
            messages.error(request,"Password does not match")
            return HttpResponseRedirect(request.path_info)
        # Create a new user
        user = MyUser.objects.create(
            full_name=full_name,
            username=username,
            email=email,
            password=password,
            is_active=True,
            category = 'student'
        )
        user.save()
        messages.success(request,"your account created successfully.")
        return redirect("/users/login_user")
    return render(request, "student/register.html")

def studadmin(request):
    user_id = request.session.get('user_id')
    print(request.session.get('user_id'))
    context = {}  # Initialize context dictionary
    
    if not user_id:
        # User is not logged in, redirect to login page
        return redirect('/users/login_user')

    # Retrieve the user object based on the user_id stored in the session
    user = MyUser.objects.filter(pk=user_id).first()

    # Check if the user exists
    if user:
        print("hi",user)
    
    context = {'user':user,"Books":"books"}
    return render(request, "student/studadmin.html", context)

def stud_logout(request): 
    request.session.flush()  
    messages.success(request,"Logged out Successfully")
    return HttpResponseRedirect('/')

def studbookIssued(request):
    user_id = request.session.get('user_id')
    print(request.session.get('user_id'))
    context = {}  # Initialize context dictionary
    
    if not user_id:
        # User is not logged in, redirect to login page
        return redirect('/users/login_user')

    # Retrieve the user object based on the user_id stored in the session
    user = MyUser.objects.filter(pk=user_id).first()

    # Check if the user exists
    if user:
        print("hi",user)
    IBR = IssuedBookRecord.objects.all()
    context = {'user':user,"IBR":IBR}
    return render(request,"student/studbookIssued.html",context)

def studbookretured(request):
    user_id = request.session.get('user_id')
    print(request.session.get('user_id'))
    context = {}  # Initialize context dictionary
    
    if not user_id:
        # User is not logged in, redirect to login page
        return redirect('/users/login_user')

    # Retrieve the user object based on the user_id stored in the session
    user = MyUser.objects.filter(pk=user_id).first()

    # Check if the user exists
    if user:
        print("hi",user)
    IBR = IssuedBookRecord.objects.all()
    context = {'user':user,"IBR":IBR}
    return render(request,"student/studbookretured.html",context)

def stud_forgetpass(request):
    if request.method == "POST":
        email = request.POST.get('email')
        
        if 'submit' in request.POST and request.POST['submit'] == 'send':
            print("send",email)
            if email is not None:
                stud=MyUser.objects.filter(email = email)
                if stud.exists():
                    stud = MyUser.objects.get(email=email)
                    
                    # subject = "Welcome to Django Wdding PLanner Pro...!!"
                    # message = "Hello"+ org.full_name + "!! \n"+ "Thank you for visiting our website \n Thanking You..! Please open Mail to verify your email address..!"
                    # from_email = settings.EMAIL_HOST_USER
                    # to_list = [org.email]
                    # send_mail(subject , message , from_email ,to_list ,fail_silently=True)
                    
                    print("pk=",stud)
                
                    context = {"stud":stud}
                    return render(request,"student/stud_forgetpass.html",context)
                else:
                    messages.success(request, "Email does not Exsist")
                    return HttpResponseRedirect("/users/stud_forgetpass")
                    
        elif 'submit' in request.POST and request.POST['submit'] == 'Reset':
                print("reset")
                if request.method == "POST":
                    new_email = request.POST.get('email')
                    new_pass =request.POST.get('password')
                    cpass = request.POST.get('cpassword')
                    print(email,new_pass,cpass)
                        
                    if email is not None:
                     # Update the password
                        if MyUser.objects.filter(email=new_email).exists():
                            org= MyUser.objects.get(email=new_email)
                            if new_pass == cpass:
                                org.password = new_pass
                                org.save()
                            else:
                                messages.error(request,"Password does not match")
                                return HttpResponseRedirect("/users/stud_forgetpass")
                        else:
                            messages.error(request,"Email is does not exists")
                            return HttpResponseRedirect("/users/stud_forgetpass")
                        
                        messages.success(request, "Password is updated successfully")
                        return HttpResponseRedirect("/users/login_user")
                    else:
                        messages.error(request, "Email is required for the Change Password.")
                        return HttpResponseRedirect(request.path_info)
    return render(request,"student/stud_forgetpass.html")

# Teacher
def Tlogin_user(request):
    if request.method == "POST":
        username1=request.POST.get('username')
        password1= request.POST.get('password')
    
        if not MyUser.objects.filter(email=username1).exists():
            messages.error(request,"Invalid email ")
            return redirect('/users/Tlogin_user') 
        
        usern = MyUser.objects.filter(email=username1).exists() 
        if usern == True:
            user=MyUser.objects.get(email=username1)
            print(user.category)
            if user.category == 'teacher':
                if user.password == password1:
                    request.session['Tech_id'] = user.pk
                    request.session['Tech_email'] = user.email
                    request.session['Tech_profile'] = user.CATEGORY_CHOICES
                    return redirect(f"/users/Techadmin")
                else:
                    messages.error(request,"Wronge Password.")
                    return HttpResponseRedirect(request.path_info)
            else:
                messages.error(request,"You are student.Login by student section.")
                return HttpResponseRedirect(request.path_info)

    return render(request,"teacher/Tlogin.html")

def reg_Tech(request):
    if request.method == "POST":
        username = request.POST.get('username')
        full_name = request.POST.get('fullname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        cpassword = request.POST.get('cpassword')

        # Check if username already exists
        if MyUser.objects.filter(username=username).exists():
            messages.error(request,'Email is Already taken')
            return HttpResponseRedirect(request.path_info)

        # Check if passwords match
        if password != cpassword:
            messages.error(request,"Password does not match")
            return HttpResponseRedirect(request.path_info)
        # Create a new user
        user = MyUser.objects.create(
            full_name=full_name,
            username=username,
            email=email,
            password=password,
            is_active=True,
            category = 'teacher'
        )
        user.save()
        messages.success(request,"your account created successfully.")
        return redirect("/users/Tlogin_user")
    return render(request,"teacher/Tregister.html")

def Techadmin(request):
    user_id = request.session.get('Tech_id')
    print(request.session.get('Tech_id'))
    context = {}  # Initialize context dictionary
    
    if not user_id:
        # User is not logged in, redirect to login page
        return redirect('/users/Tlogin_user')

    # Retrieve the user object based on the user_id stored in the session
    user = MyUser.objects.filter(pk=user_id).first()

    # Check if the user exists
    if user:
        print("hi",user)
    context = {'user':user,"Books":"books"}
    return render(request, "teacher/Techadmin.html", context)

def Tech_logout(request): 
    request.session.flush()  
    messages.success(request,"Logged out Successfully")
    return HttpResponseRedirect('/')

def TechbookIssued(request):
    user_id = request.session.get('Tech_id')
    print(request.session.get('Tech_id'))
    context = {}  # Initialize context dictionary
    
    if not user_id:
        # User is not logged in, redirect to login page
        return redirect('/users/Tlogin_user')

    # Retrieve the user object based on the user_id stored in the session
    user = MyUser.objects.filter(pk=user_id).first()

    # Check if the user exists
    if user:
        print("hi",user)
    IBR = IssuedBookRecord.objects.all()
    context = {'user':user,"IBR":IBR}
    return render(request,"teacher/TechbookIssued.html",context)

def Techbookretured(request):
    user_id = request.session.get('Tech_id')
    print(request.session.get('Tech_id'))
    context = {}  # Initialize context dictionary
    
    if not user_id:
        # User is not logged in, redirect to login page
        return redirect('/users/Tlogin_user')

    # Retrieve the user object based on the user_id stored in the session
    user = MyUser.objects.filter(pk=user_id).first()

    # Check if the user exists
    if user:
        print("hi",user)
    IBR = IssuedBookRecord.objects.all()
    context = {'user':user,"IBR":IBR}
    return render(request,"teacher/Techbookretured.html",context)

def Tech_forgetpass(request):
    if request.method == "POST":
        email = request.POST.get('email')
        
        if 'submit' in request.POST and request.POST['submit'] == 'send':
            print("send",email)
            if email is not None:
                stud=MyUser.objects.filter(email = email)
                if stud.exists():
                    stud = MyUser.objects.get(email=email)
                    
                    # subject = "Welcome to Django Wdding PLanner Pro...!!"
                    # message = "Hello"+ org.full_name + "!! \n"+ "Thank you for visiting our website \n Thanking You..! Please open Mail to verify your email address..!"
                    # from_email = settings.EMAIL_HOST_USER
                    # to_list = [org.email]
                    # send_mail(subject , message , from_email ,to_list ,fail_silently=True)
                    
                    print("pk=",stud)
                
                    context = {"stud":stud}
                    return render(request,"teacher/Tech_forgetpass.html",context)
                else:
                    messages.success(request, "Email does not Exsist")
                    return HttpResponseRedirect("/users/Tech_forgetpass")
                    
        elif 'submit' in request.POST and request.POST['submit'] == 'Reset':
                print("reset")
                if request.method == "POST":
                    new_email = request.POST.get('email')
                    new_pass =request.POST.get('password')
                    cpass = request.POST.get('cpassword')
                    print(email,new_pass,cpass)
                        
                    if email is not None:
                     # Update the password
                        if MyUser.objects.filter(email=new_email).exists():
                            org= MyUser.objects.get(email=new_email)
                            if new_pass == cpass:
                                org.password = new_pass
                                org.save()
                            else:
                                messages.error(request,"Password does not match")
                                return HttpResponseRedirect("/users/Tech_forgetpass")
                        else:
                            messages.error(request,"Email is does not exists")
                            return HttpResponseRedirect("/users/Tech_forgetpass")
                        
                        messages.success(request, "Password is updated successfully")
                        return HttpResponseRedirect("/users/Tlogin_user")
                    else:
                            messages.error(request, "Email is required for the Change Password.")
                            return HttpResponseRedirect(request.path_info)
    return render(request,"teacher/Tech_forgetpass.html")


