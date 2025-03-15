from django.shortcuts import render

# Create your views here.
from django.shortcuts import render,HttpResponseRedirect,redirect
from django.contrib import messages
from myapp.models import Book, IssuedBookRecord, MyUser,Author,Category,Fine
from django.http import JsonResponse



def booksIssued(request):
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
            rid = request.POST.get('rid')
            user = request.POST.get('user')
            book = request.POST.get('book')
            due_dateR = request.POST.get('due_date')
            Issueded_dateR = request.POST.get('Issueded_date')
            print(rid,user,book)
        
            if user is None and user=="" and book is None and due_dateR is None and Issueded_dateR is None:
                messages.error(request, "Please Enter All fields.")
                return HttpResponseRedirect(request.path_info)
            
        if 'submit' in request.POST and request.POST['submit'] == 'save':
            if IssuedBookRecord.objects.filter(user=user).exists():
                messages.error(request, "Already this student take book sorry.")
                return HttpResponseRedirect(request.path_info)
            else:
                user_obj = MyUser.objects.get(uid = user)
                book_obj = Book.objects.get(bid = book)
                IRD = IssuedBookRecord.objects.create(user = user_obj,book = book_obj,Issueded_date=Issueded_dateR,due_date=due_dateR)
                IRD.save()
                messages.success(request, "Save sucessfully.")
                return HttpResponseRedirect(request.path_info)
            
        if 'submit' in request.POST and request.POST['submit'] == 'edit':
            try:
                rec = IssuedBookRecord.objects.get(pk = rid)
                Books = Book.objects.all()
                studs = MyUser.objects.all()
                IBR = IssuedBookRecord.objects.all()  #.order_by('-Issueded_date')[:5]  # Fetch the 2 latest objects
                context = {'user':user,"Books":Books,"studs":studs,"IBR":IBR,"rec":rec}
            except Author.DoesNotExist:
                messages.error(request, "Author does not exist.")
                return HttpResponseRedirect(request.path_info)
            
            except Category.DoesNotExist:
                messages.error(request, "Category does not exist.")
                return HttpResponseRedirect(request.path_info)
            return render(request, "booksIssued.html", context)
        
        if 'submit' in request.POST and request.POST['submit'] == 'update':
            if user is None and user=="" and book is None and due_dateR is None and Issueded_dateR is None:
                messages.error(request, "Please Enter All fields.")
                return HttpResponseRedirect(request.path_info)
            try:
                userobj = MyUser.objects.get(pk = int(user))
                bookobj = Book.objects.get(pk = int(book))
                IBR = IssuedBookRecord.objects.get(pk = rid)
                IBR.user = userobj
                IBR.book = bookobj
                IBR.Issueded_date = Issueded_dateR
                IBR.due_date = due_dateR
                IBR.save()
                messages.success(request, "Issued Book Record is Updated..!")
            except MyUser.DoesNotExist:
                messages.error(request, "user does not exist.")
                return HttpResponseRedirect(request.path_info)
            
            except Book.DoesNotExist:
                messages.error(request, "Book does not exist.")
                return HttpResponseRedirect(request.path_info)
            return HttpResponseRedirect(request.path_info) 
        
        if 'submit' in request.POST and request.POST['submit'] == 'cancel':
            return HttpResponseRedirect(request.path_info) 
        
        if 'submit' in request.POST and request.POST['submit'] == 'del':
            try:
                IRB = IssuedBookRecord.objects.get(pk = rid)
                IRB.delete()
                messages.error(request, "Record is deleted successfully")
            except IssuedBookRecord.DoesNotExist:
                messages.error(request, "Record does not exist.")
                return HttpResponseRedirect(request.path_info)
            return HttpResponseRedirect(request.path_info)
            
    Books = Book.objects.all()
    studs = MyUser.objects.all()
    IBR = IssuedBookRecord.objects.all()
    context = {'user':user,"Books":Books,"studs":studs,"IBR":IBR}
    return render(request, "booksIssued.html", context)


def returnbook(request):
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
            rid = request.POST.get('rid')
            retured_date= request.POST.get('retundate')
            print(rid,user,retured_date)
        
            if retured_date is None and retured_date=="":
                messages.error(request, "Please Enter return Date.")
                return HttpResponseRedirect(request.path_info)
            
        if 'submit' in request.POST and request.POST['submit'] == 'save':
            if IssuedBookRecord.objects.filter(user=user).exists():
                IBR_obj = IssuedBookRecord.objects.get(brid = rid)
                print(IBR_obj,retured_date)
                IBR_obj.returned_date = retured_date
                IBR_obj.save()
                messages.success(request, "Save sucessfully.")
                return HttpResponseRedirect(request.path_info)
            else:
                messages.success(request, "Sorry it is not exist.")
                return HttpResponseRedirect(request.path_info)
    IBR = IssuedBookRecord.objects.all()
    context = {'user':user,"IBR":IBR}
    return render(request, "returnbook.html", context)

def manage_fine(request):
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
            rid = request.POST.get('rid')
            retured_date= request.POST.get('retundate')
            print(rid,user,retured_date)
        
            if retured_date is None and retured_date=="":
                messages.error(request, "Please Enter return Date.")
                return HttpResponseRedirect(request.path_info)
            
        if 'submit' in request.POST and request.POST['submit'] == 'fine':
            if IssuedBookRecord.objects.filter(user=user).exists():
                IBR_obj = IssuedBookRecord.objects.get(brid = rid)
                return HttpResponseRedirect('/book/Pay_fine/')
            
        if 'submit' in request.POST and request.POST['submit'] == 'save':
            if IssuedBookRecord.objects.filter(user=user).exists():
                IBR_obj = IssuedBookRecord.objects.get(brid = rid)
                print(IBR_obj,retured_date)
                IBR_obj.returned_date = retured_date
                IBR_obj.save()
                messages.success(request, "Save sucessfully.")
                return HttpResponseRedirect(request.path_info)
            else:
                messages.success(request, "Sorry it is not exist.")
                return HttpResponseRedirect(request.path_info)
            
    IBR = IssuedBookRecord.objects.all()
    fine = Fine.objects.all()
    context = {'user':user,"IBR":IBR,"fine":fine}
    return render(request, "manage_fine.html", context)

def Pay_fine(request):
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
            rid = request.POST.get('rid')
            retured_date= request.POST.get('retundate')
            Famount= request.POST.get('amount')
            uname= request.POST.get('name')
            print(rid,user,retured_date)
        
            if retured_date is None and retured_date=="":
                messages.error(request, "Please Enter return Date.")
                return HttpResponseRedirect(request.path_info)
            
        if 'submit' in request.POST and request.POST['submit'] == 'fine':
            if IssuedBookRecord.objects.filter(user=user).exists():
                IBR_obj = IssuedBookRecord.objects.get(brid = rid)
                IBR = IssuedBookRecord.objects.all()
                context = {'user':user,"IBR":IBR,"IBR_obj":IBR_obj}
                return render(request, "Pay_fine.html", context)
            else:
                messages.success(request, "Sorry it is not exist.")
                return HttpResponseRedirect(request.path_info)
        
        if 'submit' in request.POST and request.POST['submit'] == 'save':
            if IssuedBookRecord.objects.filter(user=user).exists() and fine.objects.filter(user=user).exists():
                IBR_obj = IssuedBookRecord.objects.get(brid = rid)
                userobj = MyUser.objects.get(full_name = uname)
                print(IBR_obj.user)
                fine = Fine.objects.create(borrow_record =IBR_obj, amount=Famount,paid = True)
                fine.save()
                messages.success(request, "Fine is pay successfully.")
                return HttpResponseRedirect(request.path_info)
            
        if 'submit' in request.POST and request.POST['submit'] == 'cancel':
            return HttpResponseRedirect(request.path_info)
            
    IBR = IssuedBookRecord.objects.all()
    fine = Fine.objects.all()
    context = {'user':user,"IBR":IBR,"fine":fine}
    return render(request, "Pay_fine.html", context)