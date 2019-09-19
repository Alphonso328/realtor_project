from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from .models import Contact

# Create your views here.
def contact(request):
    if request.method == 'POST':
        listing_id = request.POST['listing_id']
        listing = request.POST['listing']
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        message = request.POST['message']
        user_id = request.POST['user_id']
        employee_email = request.POST['employee_email']

        # check for Inqury
        if request.user.is_authenticated:
            user_id = request.user.id
            has_contacted = Contact.objects.all().filter(listing_id=listing_id, user_id=user_id)
            if has_contacted:
              messages.error(request, 'Your Inqury has been sent wait for reply')
              return redirect('/listings/'+ listing_id)

    
        contact = Contact(listing=listing, listing_id=listing_id, name=name, email=email, phone=phone, message=message, user_id=user_id)

        contact.save()

        #send mail
        send_mail(
            'Property Listing inquiry',
            'There has been a Inqury for ' + listing + '. Sign into admin panel for more info,',
            'g.tech350z@gmail.com',
            [employee_email, 'darkchaos350z@hotmail.com'],
            fail_silently=False
        )

        messages.success(request, 'Inquiry Submitted')

        return redirect('/listings/'+listing_id)
