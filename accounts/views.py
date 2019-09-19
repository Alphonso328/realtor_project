from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User
from contacts.models import Contact

# Create your views here.
def register(request):
    if request.method == 'POST':
       first_name = request.POST['first_name']
       last_name = request.POST['last_name']
       username = request.POST['username']
       email = request.POST['email']
       password = request.POST['password']
       password2 = request.POST['password2']

       # passsword check
       if password == password2:
          # Check username
         if User.objects.filter(username=username).exists():
             messages.error(request, ' Username Already Exists')
             return redirect('register')
         else:
            if User.objects.filter(email=email).exists():
             messages.error(request, ' Email Already Exists')
             return redirect('register')
            else:
             # looks good
             user = User.objects.create_user(username=username, email=email, first_name=first_name, last_name=last_name, password=password) 
             # Login after Registered using auth
             # auth.login(request, user)
             # messages.success(request, ' you are now logged in ')
             # return redirect('index')
             user.save()
             messages.success(request, ' you are now registered ')
             return redirect('login')
       else:
          messages.error(request,'Passwords Do Not Match')
          return redirect('register')
    else:   
      return render(request, 'accounts/register.html')

def login(request):
    if request.method == 'POST':
         # Login User
      username = request.POST['username']
      password = request.POST['password']

      user = auth.authenticate(username=username, password=password)

      if user is not None:
        auth.login(request, user)
        messages.success(request, 'Logged in')
        return redirect('dashboard')
      else:
          messages.error(request, 'Invalid Username or Password')
          return redirect('login')
    else: 
     return render(request, 'accounts/login.html')

def logout(request):
    if request.method =='POST':
      auth.logout(request)
      messages.success(request, 'You are logged out')
    return redirect('index')

def dashboard(request):
    user_contacts = Contact.objects.order_by('-contact_date').filter(user_id=request.user.id)

    context = {
      'contacts': user_contacts
    }
    return render(request, 'accounts/dashboard.html', context)
