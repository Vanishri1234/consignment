from django.shortcuts import render, reverse, redirect, get_object_or_404
from consignment_app.models import Login, AddConsignment, AddTrack,FeedBack
from django.core.mail import send_mail

import datetime
import random
import string
import secrets

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from django.conf import settings
from django.contrib.auth.hashers import make_password


#import datetime
#from .models import AddTrack, AddConsignment




# Create your views here.
def index(request):
    return render(request,'index.html')

from django.contrib import messages

def feedback(request):
    uid = request.session.get('username')
    if not uid:
        return redirect('login')  # Redirect to login if session does not have username

    # Fetch only the receiver_email column
    userdata = AddConsignment.objects.filter(receiver_email=uid).values_list('receiver_email', flat=True)

    if request.method == "POST":
        feed = request.POST.get('feedback')

        if userdata.exists():
            username = userdata[0]  # Extract the first email from the list

            FeedBack.objects.create(
                username=username,
                feedback=feed
            )
            messages.success(request, 'Feedback sent successfully')
            return redirect('feedback')
        else:
            messages.error(request, 'User not found')
            return render(request, 'feedback.html')

    return render(request, 'feedback.html')

def view_feedback(request):
    userdata=FeedBack.objects.all()
    return render(request,'view_feedback.html',{'userdata':userdata})


def index_menu(request):
    return render(request,'index_menu.html')

def admin_home(request):
    return render(request,'admin_home.html')

def user_home(request):
    return render(request,'user_home.html')

def user_home(request):
    return render(request,'user_home.html')

def user_menu(request):
    return render(request,'user_menu.html')

def nav(request):
    return render(request,'nav.html')


def userlogin(request):
    if request.method=="POST":
        username=request.POST.get('t1')
        password=request.POST.get('t2')
        request.session['username']=username
        ucount=Login.objects.filter(username=username).count()
        if ucount>=1:
            udata = Login.objects.get(username=username)
            upass = udata.password
            utype=udata.utype
            if password == upass:
                if utype == 'user':
                    return render(request,'user_home.html')
                if utype == 'admin':
                    return render(request,'admin_home.html')
            else:
                return render(request,'userlogin.html',{'msg':'Invalid Password'})
        else:
            return render(request,'userlogin.html',{'msg':'Invalid Username'})
    return render(request,'userlogin.html')

def addConsignment(request):
    if request.method == "POST":

        now = datetime.datetime.now()
        con_date = now.strftime("%Y-%m-%d")

        track_id = random.randint(111111, 999999)
        con_id = str(track_id)

        Consignment_id = random.randint(1111, 9999)
        Consignment_id = str(Consignment_id)

        send_name = request.POST.get('a1')
        send_mobile = request.POST.get('a2')
        send_email = request.POST.get('a3')
        send_address = request.POST.get('a4')
        sender_GST=request.POST.get('sendergst')
        sender_company=request.POST.get('sen_company')

        rec_name = request.POST.get('a5')
        rec_mobile = request.POST.get('a6')
        rec_email = request.POST.get('a7')
        rec_address = request.POST.get('a8')
        rec_company = request.POST.get('receiverCompany')

        product = request.POST.get('product')
        pieces = request.POST.get('pieces')
        volume_dimension = request.POST.get('volume_dimension')
        prod_gst=request.POST.get('prod_gst')
        prod_invoice=request.POST.get('prod_invoice')
        prod_price=request.POST.get('prod_price')
        packing=request.POST.get('pack')
        actual_weight=request.POST.get('aweight')

        qty=request.POST.get('qty')
        weight=float(request.POST.get('weight'))
        gst=request.POST.get('gst')
        cgst=request.POST.get('cgst')
        sgst=request.POST.get('sgst')
        freight = float(request.POST.get('freight'))
        hamali = float(request.POST.get('hamali'))
        door_charge = float(request.POST.get('door_charge'))
        st_charge = float(request.POST.get('st_charge'))

        route_from = request.POST.get('from')
        route_to = request.POST.get('to')

        cost = float(request.POST.get('cost'))

        pay_status = 'Paid' if request.POST.get('payment') == 'Paid' else 'Pending'


        AddConsignment.objects.create(track_id=con_id,
                                      Consignment_id=Consignment_id,
                                      sender_name=send_name,
                                      sender_mobile=send_mobile,
                                      sender_email=send_email,
                                      sender_address=send_address,
                                      sender_GST=sender_GST,
                                      sender_company=sender_company,
                                      receiver_name=rec_name,
                                      receiver_mobile=rec_mobile,
                                      receiver_email=rec_email,
                                      receiver_address=rec_address,
                                      receiver_company=rec_company,

                                      desc_product=product,
                                      pieces=pieces,
                                      dimension=volume_dimension,
                                      prod_gst=prod_gst,
                                      prod_invoice=prod_invoice,
                                      prod_price=prod_price,
                                      packing=packing,
                                      actual_weight=actual_weight,

                                      qty=qty,
                                      weight=weight,
                                      gst=gst,
                                      cgst=cgst,
                                      sgst=sgst,
                                      freight=freight,
                                      hamali=hamali,
                                      door_charge=door_charge,
                                      st_charge=st_charge,

                                      route_from=route_from,
                                      route_to=route_to,
                                      total_cost=cost,
                                      date=con_date,
                                      pay_status=pay_status)
        # Generate a random password
        alphabet = string.ascii_letters + string.digits
        password = ''.join(secrets.choice(alphabet) for i in range(8))

        # Check if the user already exists
        user, created = Login.objects.update_or_create(
            username=rec_email,
            defaults={
                'password': password,  # Store the password directly
                'utype': 'user'
            }
        )

        if created:
            print("New user created with password:", password)
        else:
            print("User already exists. Updated password to:", password)

        # Send email with consignment details
        email_subject = "Consignment Details"
        site_url = settings.SITE_URL
        home_url =  f"{site_url}{reverse('index')}"  # Ensure the URL is complete
        email_body = (
            f"Dear {rec_name},\n\n"
            f"Your consignment has been successfully added with the following details:\n\n"
            f"Sender Name: {send_name}\n"
            f"Sender Mobile: {send_mobile}\n"
            f"Sender Address: {send_address}\n\n"
            f"Receiver Name: {rec_name}\n"
            f"Receiver Mobile: {rec_mobile}\n"
            f"Receiver Address: {rec_address}\n"
            f"Receiver Address: {rec_company}\n"
            f"Receiver Address: {product}\n"
            f"Total Amount: {cost}\n\n"
            f"Track Number: {con_id}\n\n"
            f"Login Details:\n"
            f"Username: {rec_email}\n"
            f"Password: {password}\n\n"
            f"Link: {home_url}\n\n"
            f"Thank you for using our service.\n"
        )

        # Set up the SMTP server
        smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        smtp_server.ehlo()
        smtp_server.login('vanishrivanishri10593@gmail.com', 'hlpd aozl czwl mdon')

        # Send the email
        try:
            msg = MIMEMultipart()
            msg['From'] = 'Consignment <vanishrivanishri10593@gmail.com>'
            msg['To'] = rec_email
            msg['Subject'] = email_subject
            msg.attach(MIMEText(email_body, 'plain'))

            smtp_server.sendmail('vanishrivanishri10593@gmail.com', rec_email, msg.as_string())
        except Exception as e:
            print(f"Error sending email: {e}")
        finally:
            smtp_server.close()

        return redirect('printConsignment', track_id=con_id)
    return render(request, 'addConsignment.html')

def printConsignment(request, track_id):
    consignment = get_object_or_404(AddConsignment, track_id=track_id)
    return render(request, 'printConsignment.html', {'consignment': consignment})

def invoiceConsignment(request, pk):
    consignment = get_object_or_404(AddConsignment, id=pk)
    return render(request, 'invoiceConsignment.html', {'consignment': consignment})

def view_consignment(request):
    userdata=AddConsignment.objects.all()
    return render(request,'view_consignment.html',{'userdata':userdata})

def user_view_consignment(request):
    uid = request.session['username']
    userdata = AddConsignment.objects.filter(receiver_email=uid).values()
    return render(request,'user_view_consignment.html',{'userdata':userdata})


def consignment_edit(request, pk):
    userdata = AddConsignment.objects.filter(id=pk).first()  # Retrieve a single object or None


    if request.method == "POST":
        track_id = userdata.track_id
        con_date = userdata.date

        send_name = request.POST.get('a1')
        send_mobile = request.POST.get('a2')
        send_email = request.POST.get('a3')
        send_address = request.POST.get('a4')

        rec_name = request.POST.get('a5')
        rec_mobile = request.POST.get('a6')
        rec_email = request.POST.get('a7')
        rec_address = request.POST.get('a8')

        cost = request.POST.get('a9')

        # Update the object
        userdata.track_no = track_id
        userdata.sender_name = send_name
        userdata.sender_mobile = send_mobile
        userdata.sender_email = send_email
        userdata.sender_address = send_address
        userdata.receiver_name = rec_name
        userdata.receiver_mobile = rec_mobile
        userdata.receiver_email = rec_email
        userdata.receiver_address = rec_address
        userdata.total_cost = cost
        userdata.date = con_date
        userdata.save()

        # Redirect to a different URL after successful update
        base_url = reverse('view_consignment')
        return redirect(base_url)

    return render(request, 'consignment_edit.html', {'userdata': userdata})


def consignment_delete(request,pk):
    udata=AddConsignment.objects.get(id=pk)
    udata.delete()
    base_url=reverse('view_consignment')
    return redirect(base_url)




def addTrack(request):
    consignments = AddConsignment.objects.all().order_by('-id')  # Fetch all consignments ordered by id descending
    if request.method == "POST":
        now = datetime.datetime.now()
        con_date = now.strftime("%Y-%m-%d")

        track_id = request.POST.get('a1')
        status = request.POST.get('status')  # Retrieve status from the form

        # Retrieve total_cost from AddConsignment table based on some condition
        # For example, you can get it based on track_id or any other criteria

        # If the selected status is "Other", retrieve the custom status from the form
        if status == "Other":
            custom_status = request.POST.get('a2')
        else:
            custom_status = None

        # Create AddTrack object with retrieved total_cost
        AddTrack.objects.create(
            track_id=track_id,
            description=status,
            date=con_date

        )

        return render(request, 'addTrack.html', {'msg': 'Added'})
    return render(request, 'addTrack.html',{'consignments':consignments})


def search_results(request):
    tracker_id = request.GET.get('tracker_id')
    consignments = AddConsignment.objects.all().order_by('-id')  # Fetch all consignment data

    if tracker_id:
        try:
            trackers = AddTrack.objects.filter(track_id=tracker_id)
            if trackers.exists():
                return render(request, 'search_results.html', {'trackers': trackers, 'consignments': consignments})
            else:
                message = f"No tracking information found for ID: {tracker_id}"
                return render(request, 'search_results.html', {'message': message, 'consignments': consignments})
        except Exception as e:
            message = f"Error occurred: {str(e)}"
            return render(request, 'search_results.html', {'message': message, 'consignments': consignments})
    else:
        return render(request, 'search_results.html', {'message': "Please enter a tracker ID.", 'consignments': consignments})



def track_delete(request,pk):
    udata=AddTrack.objects.get(id=pk)
    udata.delete()
    base_url=reverse('search_results')
    return redirect(base_url)


def user_search_results(request):
    tracker_id = request.GET.get('tracker_id')

    if tracker_id:
        try:
            trackers = AddTrack.objects.filter(track_id=tracker_id)
            if trackers.exists():
                return render(request, 'user_search_results.html', {'trackers': trackers})
            else:
                message = f"No tracking information found for ID: {tracker_id}"
                return render(request, 'user_search_results.html', {'message': message})
        except Exception as e:
            message = f"Error occurred: {str(e)}"
            return render(request, 'user_search_results.html', {'message': message})
    else:
        return render(request, 'user_search_results.html', {'message': "Please enter a tracker ID."})
