from django.shortcuts import render,HttpResponseRedirect,redirect
from django.contrib import messages
from myapp.models import Book, MyUser,Author,Category,IssuedBookRecord
from django.http import JsonResponse
from django.db.models.functions import TruncDate
from django.db.models import Count
import json


# Create your views here.
# Admin
def admin_login(request):
    if request.method == "POST":
        username1=request.POST.get('username')
        password1= request.POST.get('password')
    
        if not MyUser.objects.filter(username=username1).exists():
            messages.error(request,"Invalid Username ")
            return redirect('/myadmin/admin_login') 
        
        usern = MyUser.objects.filter(username=username1).exists()
        if usern == True:
            user=MyUser.objects.get(username=username1)
            if user.password == password1:
                request.session['Admin_id'] = user.pk
                request.session['Admin_email'] = user.email
                return redirect(f"/myadmin/adminpanel")
            else:
                messages.error(request,"Wronge Password.")
                return HttpResponseRedirect(request.path_info) 

    return render(request,"admin_login.html")

def adminpanel(request):
    user_id = request.session.get('Admin_id')
    print(request.session.get('Admin_id'))
    context = {}  # Initialize context dictionary
    
    if not user_id:
        # User is not logged in, redirect to login page
        return redirect('/myadmin/admin_login')

    # Retrieve the user object based on the user_id stored in the session
    user = MyUser.objects.filter(pk=user_id).first()

    # Check if the user exists
    if user:
        chart_data = (
            IssuedBookRecord.objects.annotate(date=TruncDate("Issueded_date"))  # Truncate to Date
            .values("date")   # Group by Date
            .annotate(y=Count("brid"))  # Count issued books
            .order_by("-date")  # Order by latest date
        )
        # Convert queryset to JSON
        chart_data_json = json.dumps(list(chart_data), default=str)  


        cbooks = Book.objects.all().count()
        cstud = MyUser.objects.filter(category = 'student').count()
        cTech = MyUser.objects.filter(category = "teacher").count()
        Auther = Author.objects.all().count()
        
        print("chart_data=",chart_data)
    context = {'user':user,'chart_data':chart_data_json,"cbooks":cbooks,"cstud":cstud,"cTech":cTech,"Auther":Auther}
    return render(request, "index.html", context)

def addauthor(request):
    user_id = request.session.get('Admin_id')
    print(request.session.get('Admin_id'))
    context = {}  # Initialize context dictionary
    
    if not user_id:
        # User is not logged in, redirect to login page
        return redirect('/myadmin/admin_login')

    # Retrieve the user object based on the user_id stored in the session
    user = MyUser.objects.filter(pk=user_id).first()

    # Check if the user exists
    if user:
        if request.method == "POST":
            aname = request.POST.get('name')
            dob = request.POST.get('dob')
            autid = request.POST.get('aid')
            print(autid,"$$")
        if 'submit' in request.POST and request.POST['submit'] == 'save':
            aut = Author.objects.create(name = aname, birth_date=dob)
            aut.save()
            messages.success(request, "Auther is save.")
            return HttpResponseRedirect(request.path_info)
        if 'submit' in request.POST and request.POST['submit'] == 'edit':
            aut = Author.objects.get(aid = autid)
            author = Author.objects.all()
            context = {'user':user,"author":author,"aut":aut}
            return render(request, "addauthor.html", context)
        
        if 'submit' in request.POST and request.POST['submit'] == 'update':
            aut = Author.objects.get(aid = autid)
            aut.name = aname
            aut.birth_date=dob
            aut.save()
            messages.success(request, "Auther is Updated..!")
            return HttpResponseRedirect(request.path_info) 
        
        if 'submit' in request.POST and request.POST['submit'] == 'cancel':
            return HttpResponseRedirect(request.path_info) 
        
        if 'submit' in request.POST and request.POST['submit'] == 'del':
            aut = Author.objects.get(aid = autid)
            aut.delete()
            messages.error(request, "Author is deleted successfully")
        
        author = Author.objects.all()
    context = {'user':user,"author":author}
    return render(request, "addauthor.html", context)

def addcat(request):
    user_id = request.session.get('Admin_id')
    print(request.session.get('Admin_id'))
    context = {}  # Initialize context dictionary
    
    if not user_id:
        # User is not logged in, redirect to login page
        return redirect('/myadmin/admin_login')

    # Retrieve the user object based on the user_id stored in the session
    user = MyUser.objects.filter(pk=user_id).first()

    # Check if the user exists
    if user:
        if request.method == "POST":
            cname = request.POST.get('name')
            cid = request.POST.get('cid')
            print(cid,"$$")
        if 'submit' in request.POST and request.POST['submit'] == 'save':
            cat = Category.objects.create(name = cname)
            cat.save()
            messages.success(request, "Auther is save.")
            return HttpResponseRedirect(request.path_info)
        if 'submit' in request.POST and request.POST['submit'] == 'edit':
            cat = Category.objects.get(pk = cid)
            catname = Category.objects.all()
            context = {'user':user,"Category":catname,"cat":cat}
            return render(request, "addcategory.html", context)
        
        if 'submit' in request.POST and request.POST['submit'] == 'update':
            print(cid,"cid update")
            cat = Category.objects.get(pk = cid)
            cat.name = cname
            cat.save()
            messages.success(request, "Category is Updated..!")
            return HttpResponseRedirect(request.path_info) 
        
        if 'submit' in request.POST and request.POST['submit'] == 'cancel':
            return HttpResponseRedirect(request.path_info) 
        
        if 'submit' in request.POST and request.POST['submit'] == 'del':
            aut = Category.objects.get(pk = cid)
            aut.delete()
            messages.error(request, "Category is deleted successfully")
        
        mycat = Category.objects.all()
    context = {'user':user,"Category":mycat}
    return render(request, "addcategory.html", context)

def addbook(request):
    user_id = request.session.get('Admin_id')
    print(request.session.get('Admin_id'))
    context = {}  # Initialize context dictionary
    
    if not user_id:
        # User is not logged in, redirect to login page
        return redirect('/myadmin/admin_login')

    # Retrieve the user object based on the user_id stored in the session
    user = MyUser.objects.filter(pk=user_id).first()

    # Check if the user exists
    if user:
        if request.method == "POST":
            bookid = request.POST.get('bid')
            titlename = request.POST.get('title')
            bauthor = request.POST.get('author')
            bcategory = request.POST.get('cat')
            bisbn = request.POST.get('isbn')
            bpublished_date = request.POST.get('published_date')
            btotal_copies = request.POST.get('total_copies')
            bavailable_copies = request.POST.get('available_copies')
            
            
        if 'submit' in request.POST and request.POST['submit'] == 'save':
            if titlename is None and not bauthor and not bcategory and not bisbn and not bpublished_date and not btotal_copies and not bavailable_copies:
                messages.success(request, "All fields are required.")
                return HttpResponseRedirect(request.path_info)
            if Book.objects.filter(isbn=bisbn).exists():
                messages.error(request, "A book with this ISBN already exists.")
                return HttpResponseRedirect(request.path_info)

            # Check if the book title already exists (optional check based on your logic)
            if Book.objects.filter(title=titlename).exists():
                messages.error(request, "A book with this title already exists.")
                return HttpResponseRedirect(request.path_info)

            try:
                # Fetch Author and Category objects
                autobj = Author.objects.get(pk=bauthor)
                catobj = Category.objects.get(pk=bcategory)

                # Create new Book object and save to the database
                mybook = Book.objects.create(
                    title=titlename,
                    author=autobj,
                    category=catobj,
                    isbn=bisbn,
                    published_date=bpublished_date,
                    total_copies=btotal_copies,
                    available_copies=bavailable_copies
                )

                mybook.save()

                messages.success(request, "Book is saved.")
                return HttpResponseRedirect(request.path_info)

            except Author.DoesNotExist:
                messages.error(request, "Author does not exist.")
                return HttpResponseRedirect(request.path_info)
            
            except Category.DoesNotExist:
                messages.error(request, "Category does not exist.")
                return HttpResponseRedirect(request.path_info)
            
        if 'submit' in request.POST and request.POST['submit'] == 'edit':
            try:
                mybook = Book.objects.get(pk = bookid)
                mycat = Category.objects.all()
                books = Book.objects.all().order_by('-bid')[:5]  # Fetch the 2 latest objects
                author = Author.objects.all()
                context = {'user':user,"Category":mycat,"Books":books,"authors":author,"mybook":mybook}
            except Author.DoesNotExist:
                messages.error(request, "Author does not exist.")
                return HttpResponseRedirect(request.path_info)
            
            except Category.DoesNotExist:
                messages.error(request, "Category does not exist.")
                return HttpResponseRedirect(request.path_info)
            return render(request, "addbook.html", context)
        
        if 'submit' in request.POST and request.POST['submit'] == 'update':
            if bauthor is None and bcategory is None and bpublished_date is None :
                messages.success(request, "All fields are required.")
            try:
                autobj = Author.objects.get(pk = bauthor)
                catobj = Category.objects.get(pk = bcategory)
                book = Book.objects.get(pk = bookid)
                book.title = titlename
                book.author = autobj
                book.category = catobj
                book.published_date = bpublished_date
                book.total_copies = btotal_copies
                book.available_copies = bavailable_copies
                book.save()
                messages.success(request, "Book is Updated..!")
            except Author.DoesNotExist:
                messages.error(request, "Author does not exist.")
                return HttpResponseRedirect(request.path_info)
            
            except Category.DoesNotExist:
                messages.error(request, "Category does not exist.")
                return HttpResponseRedirect(request.path_info)
            return HttpResponseRedirect(request.path_info) 
        
        if 'submit' in request.POST and request.POST['submit'] == 'cancel':
            return HttpResponseRedirect(request.path_info) 
        
        if 'submit' in request.POST and request.POST['submit'] == 'del':
            try:
                book = Book.objects.get(pk = bookid)
                book.delete()
                messages.error(request, "Book is deleted successfully")
            except Book.DoesNotExist:
                messages.error(request, "Book does not exist.")
                return HttpResponseRedirect(request.path_info)
            return HttpResponseRedirect(request.path_info)
        
        mycat = Category.objects.all()
        books = Book.objects.all().order_by('-bid')[:5]  # Fetch the 2 latest objects
        author = Author.objects.all()
    context = {'user':user,"Category":mycat,"Books":books,"authors":author}
    return render(request, "addbook.html", context)

def viewbooks(request):
    user_id = request.session.get('Admin_id')
    print(request.session.get('Admin_id'))
    context = {}  # Initialize context dictionary
    
    if not user_id:
        # User is not logged in, redirect to login page
        return redirect('/myadmin/admin_login')

    # Retrieve the user object based on the user_id stored in the session
    user = MyUser.objects.filter(pk=user_id).first()

    # Check if the user exists
    if user:
        books = Book.objects.all()
        if request.method == "POST":
            bookid = request.POST.get('bid')
            titlename = request.POST.get('title')
            bauthor = request.POST.get('author')
            bcategory = request.POST.get('cat')
            bisbn = request.POST.get('isbn')
            bpublished_date = request.POST.get('published_date')
            btotal_copies = request.POST.get('total_copies')
            bavailable_copies = request.POST.get('available_copies')
        
        if 'submit' in request.POST and request.POST['submit'] == 'edit':
            try:
                mybook = Book.objects.get(pk = bookid)
                mycat = Category.objects.all()
                books = Book.objects.all().order_by('-bid')[:5]  # Fetch the 2 latest objects
                author = Author.objects.all()
                context = {'user':user,"Category":mycat,"Books":books,"authors":author,"mybook":mybook}
            except Author.DoesNotExist:
                messages.error(request, "Author does not exist.")
                return HttpResponseRedirect(request.path_info)
            
            except Category.DoesNotExist:
                messages.error(request, "Category does not exist.")
                return HttpResponseRedirect(request.path_info)
            return render(request, "addbook.html", context)
        
        if 'submit' in request.POST and request.POST['submit'] == 'update':
            if bauthor is None and bcategory is None and bpublished_date is None :
                messages.success(request, "All fields are required.")
            try:
                autobj = Author.objects.get(pk = bauthor)
                catobj = Category.objects.get(pk = bcategory)
                book = Book.objects.get(pk = bookid)
                book.title = titlename
                book.author = autobj
                book.category = catobj
                book.published_date = bpublished_date
                book.total_copies = btotal_copies
                book.available_copies = bavailable_copies
                book.save()
                messages.success(request, "Book is Updated..!")
            except Author.DoesNotExist:
                messages.error(request, "Author does not exist.")
                return HttpResponseRedirect(request.path_info)
            
            except Category.DoesNotExist:
                messages.error(request, "Category does not exist.")
                return HttpResponseRedirect(request.path_info)
            return HttpResponseRedirect(request.path_info) 
        
        if 'submit' in request.POST and request.POST['submit'] == 'cancel':
            return HttpResponseRedirect(request.path_info) 
        
        if 'submit' in request.POST and request.POST['submit'] == 'del':
            try:
                book = Book.objects.get(pk = bookid)
                book.delete()
                messages.error(request, "Book is deleted successfully")
            except Book.DoesNotExist:
                messages.error(request, "Book does not exist.")
                return HttpResponseRedirect(request.path_info)
            return HttpResponseRedirect(request.path_info)
            
    context = {'user':user,"books":books}
    return render(request, "viewbook.html", context)

def admin_logout(request): 
    request.session.flush()  
    messages.success(request,"Logged out Successfully")
    return HttpResponseRedirect('/')

def admin_forgetpass(request): 
    if request.method == "POST":
        email = request.POST.get('email')
        
        if 'submit' in request.POST and request.POST['submit'] == 'send':
            print("send",email)
            if email is not None:
                orgnizer=MyUser.objects.filter(email = email)
                if orgnizer.exists():
                    org = MyUser.objects.get(email=email)
                    
                    # subject = "Welcome to Django Wdding PLanner Pro...!!"
                    # message = "Hello"+ org.full_name + "!! \n"+ "Thank you for visiting our website \n Thanking You..! Please open Mail to verify your email address..!"
                    # from_email = settings.EMAIL_HOST_USER
                    # to_list = [org.email]
                    # send_mail(subject , message , from_email ,to_list ,fail_silently=True)
                    
                    print("pk=",org)
                
                    context = {"org":org}
                    return render(request,"adforgetpass.html",context)
                else:
                    messages.success(request, "Email does not Exsist")
                    return HttpResponseRedirect("/myadmin/admin_forgetpass")
                    
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
                                return HttpResponseRedirect("/myadmin/admin_forgetpass")
                        else:
                            messages.error(request,"Email is does not exists")
                            return HttpResponseRedirect("/myadmin/admin_forgetpass")
                        
                        messages.success(request, "Password is updated successfully")
                        return HttpResponseRedirect("/myadmin/admin_forgetpass")
                    else:
                            messages.error(request, "Email is required for the Change Password.")
                            return HttpResponseRedirect(request.path_info)
    
    return render(request,"adforgetpass.html")

def studManage(request):
    user_id = request.session.get('Admin_id')
    print(request.session.get('Admin_id'))
    context = {}  # Initialize context dictionary
    
    if not user_id:
        # User is not logged in, redirect to login page
        return redirect('/myadmin/admin_login')

    # Retrieve the user object based on the user_id stored in the session
    user = MyUser.objects.filter(pk=user_id).first()

    # Check if the user exists
    if user:
        if request.method == "POST":
            id = request.POST.get('uid')
            
            if 'submit' in request.POST and request.POST['submit'] == 'del':
                deluser = MyUser.objects.get(uid=id)
                deluser.delete()
                messages.success(request, "Student is deleted successfully")
        stud = MyUser.objects.filter(category ='student')
        print(stud)
    context = {"stud":stud}
    return render(request,"studManage.html",context)

def TechManage(request):
    user_id = request.session.get('Admin_id')
    print(request.session.get('Admin_id'))
    context = {}  # Initialize context dictionary
    
    if not user_id:
        # User is not logged in, redirect to login page
        return redirect('/myadmin/admin_login')

    # Retrieve the user object based on the user_id stored in the session
    user = MyUser.objects.filter(pk=user_id).first()

    # Check if the user exists
    if user:
        if request.method == "POST":
            id = request.POST.get('uid')
            
            if 'submit' in request.POST and request.POST['submit'] == 'del':
                deluser = MyUser.objects.get(uid=id)
                deluser.delete()
                messages.success(request, "Teacher is deleted successfully")
    tech = MyUser.objects.filter(category ='teacher')
    context = {"tech":tech}
    return render(request,"TechManage.html",context)