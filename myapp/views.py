from django.shortcuts import render,HttpResponseRedirect,redirect
from django.contrib import messages
from .models import Contact
# Create your views here.

#This function will add new item and show all items
def homepage(request): 
   return render(request,"base.html")
     
def about(request):
   context = {"about":"about"} 
   return render(request,"about.html",context)

def contact(request): 
        if request.method == 'POST':
           name = request.POST.get("name")
           msg = request.POST.get("message") 
           email = request.POST.get("email")    
           
           if 'submit' in request.POST and request.POST['submit'] == 'save':
               try:
                  if Contact.objects.filter(cemail=email).exists():
                     messages.error(request,"Your feedback has already been recorded. Sorry.")
                     return HttpResponseRedirect(request.path_info)
                  else:
                     cm = Contact.objects.create(cname = name,cemail=email,cmsg = msg)
                     cm.save()
                     messages.error(request,"Thank you for you feedback.")
                     return HttpResponseRedirect(request.path_info)
                  
               except Exception as e:
                  print(e)
                  return HttpResponseRedirect(request.path_info)
           
        context = {"contact":"contact"}
        return render(request,"contact.html",context)
