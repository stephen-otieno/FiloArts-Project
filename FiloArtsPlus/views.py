import json

# from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from FiloArtsPlus.models import Client, Drawing,Transaction, Blog, Comment

# from .forms import CustomLoginForm
from .forms import RegisterForm,CustomLoginForm,BlogForm, CommentForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.core.mail import send_mail
from datetime import datetime
import base64
import requests





def index(request):
    return render(request, 'index.html')

def gallery(request):
    drawings = Drawing.objects.all()
    return render(request, 'gallery.html', {'drawings':drawings})

# def blogs(request):
#     return render(request, 'blogs.html')


# Function for fetching and plotting the clients details on the database
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Client  # Ensure Client model exists

def client_data(request):
    if request.method == 'POST':
        client_name = request.POST.get('client_name', '').strip()
        client_email = request.POST.get('client_email', '').strip()
        client_message = request.POST.get('client_message', '').strip()

        if not client_name or not client_email or not client_message:
            messages.error(request, "All fields are required!")
        else:
            Client.objects.create(
                client_name=client_name,
                client_email=client_email,
                client_message=client_message
            )
            messages.success(request, "Your message has been sent successfully!")

        return redirect('/')  # Redirects back to the homepage

    return render(request, 'index.html')

# Function for the clients table

@login_required(login_url='login')
def view_clients(request):
    clients = Client.objects.all()
    return render(request, 'clients.html', {'clients':clients})


def login_page(request):
    if request.method == 'POST':
        form = CustomLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('clients')  # Redirect to the home page after successful login
    else:
        form = CustomLoginForm()

    return render(request, 'login.html',{'form':form})




# Function to capture and plot drawing uploads

@login_required(login_url='login')
def drawing_upload(request):
    if request.method == 'POST':
        drawing_name = request.POST['drawing_name']
        drawing_artist = request.POST['drawing_artist']
        drawing_price = request.POST['drawing_price']
        drawing_img = request.FILES['drawing_img']

        drawing = Drawing(
            drawing_name=drawing_name,
            drawing_artist=drawing_artist,
            drawing_price=drawing_price,
            drawing_img=drawing_img,

        )

        drawing.save()
        return redirect('/')

    return render(request, 'drawing_upload.html')


class MpesaPassword:
    @staticmethod
    def generate_security_credential():
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')

        business_short_code = '174379'
        passkey = 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919'
        data_to_encode = business_short_code + passkey + timestamp
        online_password = base64.b64encode(data_to_encode.encode()).decode('utf-8')

        return online_password


CONSUMER_KEY = 'jkXBgjW27IKhblgEVsR5SOfTh6Am0MZ3IWs1xTPIyKgLA70x'
CONSUMER_SECRET = 'z6WM04Fv88SyG8QeSgtva1GXdNyWPpbOi6vTNuEbuA6aL64l6sqAzxqpePAEXYvG'
SHORTCODE = '174379'
PASSKEY = 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919'
BASE_URL = 'https://sandbox.safaricom.co.ke'



def generate_access_token():
    auth_url = f'{BASE_URL}/oauth/v1/generate?grant_type=client_credentials'
    response = requests.get(auth_url, auth=(CONSUMER_KEY, CONSUMER_SECRET))
    return response.json().get('access_token')



@csrf_exempt
def stk_push(request):
    if request.method == 'POST':
        phone = request.POST.get('phone')
        amount = request.POST.get('amount')
        name = request.POST.get('name')
        email = request.POST.get('email')

        transaction = Transaction.objects.create(
            phone_number=phone,
            amount=amount,
            status="Pending",
            description="Awaiting callback",
            name=name,
            email=email,
        )

        access_token = generate_access_token()
        stk_url = f'{BASE_URL}/mpesa/stkpush/v1/processrequest'
        headers = {'Authorization': f'Bearer {access_token}', 'Content-Type': 'application/json'}

        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        password = base64.b64encode(f'{SHORTCODE}{PASSKEY}{timestamp}'.encode()).decode()

        payload = {
            "BusinessShortCode": SHORTCODE,
            "Password": password,
            "Timestamp": timestamp,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,
            "PartyA": phone,
            "PartyB": SHORTCODE,
            "PhoneNumber": phone,
            "CallBackURL": "https://b6ec-217-199-146-223.ngrok-free.app/callback",
            "AccountReference": f"Transaction_{transaction.id}",
            "TransactionDesc": "Payment for services"
        }

        response = requests.post(stk_url, json=payload, headers=headers)
        response_data = response.json()

        transaction_id = response_data.get('CheckoutRequestID', None)
        transaction.transaction_id = transaction_id
        transaction.description = response_data.get('ResponseDescription', 'No description')
        transaction.save()

        return redirect('waiting_page', transaction_id=transaction.id)

    return JsonResponse({"error": "Invalid request"}, status=400)



def waiting_page(request, transaction_id):
    transaction = Transaction.objects.get(id=transaction_id)
    return render(request, 'waiting.html', {'transaction_id': transaction_id})



def check_status(request, transaction_id):
    transaction = Transaction.objects.filter(id=transaction_id).first()

    if not transaction:
        return JsonResponse({"status": "Failed", "message": "Transaction not found"}, status=404)

    if transaction.status == "Success":
        return JsonResponse({"status": "Success", "message": "Payment Successful"})
    elif transaction.status == "Failed":
        return JsonResponse({"status": "Failed", "message": "Payment Failed"})
    elif transaction.status == "Cancelled":
        return JsonResponse({"status": "Cancelled", "message": "Transaction was cancelled by the user"})
    else:
        return JsonResponse(
            {"status": "Unknown", "message": "Transaction is still being processed or status is unknown"})




@csrf_exempt
def callback(request):
    if request.method != 'POST':
        return JsonResponse({"error": "Invalid request method"}, status=400)

    try:
        data = json.loads(request.body)
        print("Received callback data:", data)

        stk_callback = data.get('Body', {}).get('stkCallback', {})
        result_code = stk_callback.get('ResultCode')
        result_desc = stk_callback.get('ResultDesc', '')
        transaction_id = stk_callback.get('CheckoutRequestID')

        if not transaction_id:
            print("Missing transaction ID in callback")
            return JsonResponse({"error": "Missing transaction ID"}, status=400)

        transaction = Transaction.objects.filter(transaction_id=transaction_id).first()
        if not transaction:
            print(f"Transaction {transaction_id} not found.")
            return JsonResponse({"error": "Transaction not found"}, status=404)

        if result_code == 0:
            callback_metadata = stk_callback.get('CallbackMetadata', {}).get('Item', [])
            receipt_number = next((item.get('Value') for item in callback_metadata if item.get('Name') == 'MpesaReceiptNumber'), None)
            amount = next((item.get('Value') for item in callback_metadata if item.get('Name') == 'Amount'), None)
            transaction_date_str = next((item.get('Value') for item in callback_metadata if item.get('Name') == 'TransactionDate'), None)

            transaction_date = datetime.strptime(str(transaction_date_str), "%Y%m%d%H%M%S") if transaction_date_str else None

            transaction.mpesa_receipt_number = receipt_number
            transaction.transaction_date = transaction_date
            transaction.amount = amount
            transaction.status = "Success"
            transaction.description = "Payment successful"
            transaction.save()

            print(f"Transaction {transaction_id} updated successfully.")

            # Send confirmation email
            if transaction.email:
                subject = "Payment Receipt Confirmation"
                message = f"""
                Dear {transaction.name},

                Thank you for your payment of {transaction.amount}.
                Your Mpesa transaction code is {transaction.mpesa_receipt_number}.

                Should you have any questions, please contact us:
                Phone: 0115598800
                Powered by Stemiot Innovations (https://stemiotsoftwares.onrender.com/)

                Best regards,
                Stemiot Innovations
                """
                html_message = f"""
                <p>Dear {transaction.name},</p>
                <p>Thank you for your payment of {transaction.amount}.</p>
                <p>Your receipt number is <strong>{transaction.mpesa_receipt_number}</strong>.</p>
                <p>Should you have any questions, please feel free to reach us at:</p>
                <p><strong>Phone:</strong> 0115598800</p>
                <p>Powered by <a href='https://stemiotsoftwares.onrender.com/' target='_blank'>Stemiot Innovations</a></p>
                <p>Best regards,<br>Stemiot Innovations</p>
                """
                send_mail(
                    subject,
                    message,
                    'engineerotienoduor14@gmail.com',
                    [transaction.email],
                    fail_silently=False,
                    html_message=html_message,
                )
                print("Payment receipt email sent.")

        elif result_code == 1:
            transaction.status = "Failed"
            transaction.description = result_desc
            transaction.save()
            print(f"Transaction {transaction_id} failed: {result_desc}")

        elif result_code == 1032:
            transaction.status = "Cancelled"
            transaction.description = "Transaction cancelled by user"
            transaction.save()
            print(f"Transaction {transaction_id} cancelled.")

        else:
            print(f"Unhandled ResultCode: {result_code} - {result_desc}")
            transaction.status = "Unknown"
            transaction.description = f"Unhandled status: {result_desc}"
            transaction.save()

        return JsonResponse({"message": "Callback processed successfully"}, status=200)

    except json.JSONDecodeError:
        print("Invalid JSON data received")
        return JsonResponse({"error": "Invalid JSON format"}, status=400)
    except Exception as e:
        print(f"Error processing callback: {e}")
        return JsonResponse({"error": "Internal server error"}, status=500)

# def callback(request):
#     if request.method == 'POST':
#         try:
#
#             data = json.loads(request.body)
#             print("Received callback data:", data)
#
#             stk_callback = data.get('Body', {}).get('stkCallback', {})
#             result_code = stk_callback.get('ResultCode', None)
#             result_desc = stk_callback.get('ResultDesc', '')
#             transaction_id = stk_callback.get('CheckoutRequestID', None)
#
#             if transaction_id:
#                 transaction = Transaction.objects.filter(transaction_id=transaction_id).first()
#                 if transaction:
#                     if result_code == 0:
#                         callback_metadata = stk_callback.get('CallbackMetadata', {}).get('Item', [])
#                         receipt_number = next((item.get('Value') for item in callback_metadata if
#                                                item.get('Name') == 'MpesaReceiptNumber'), None)
#                         amount = next((item.get('Value') for item in callback_metadata if item.get('Name') == 'Amount'),
#                                       None)
#                         transaction_date_str = next(
#                             (item.get('Value') for item in callback_metadata if item.get('Name') == 'TransactionDate'),
#                             None)
#
#                         transaction_date = None
#                         if transaction_date_str:
#                             transaction_date = datetime.strptime(str(transaction_date_str), "%Y%m%d%H%M%S")
#
#                         transaction.mpesa_receipt_number = receipt_number
#                         transaction.transaction_date = transaction_date
#                         transaction.amount = amount
#                         transaction.status = "Success"
#                         transaction.description = "Payment successful"
#                         transaction.save()
#
#                         print(f"Transaction {transaction_id} updated as successful.")
#
#                         if transaction.email:
#                             subject = "Payment Receipt Confirmation"
#                             message = (
#                                 f"Dear {transaction.name},\n\n"
#                                 f"Thank you for your payment of {transaction.amount}.\n"
#                                 f"Your Mpesa transaction code is {transaction.mpesa_receipt_number}.\n\n"
#                                 "Should you have any questions, please feel free to reach us at:\n"
#                                 "Phone: 0115598800\n"
#                                 "Powered by [Stemiot Innovations](https://stemiotsoftwares.onrender.com/)\n\n"
#                                 "Best regards,\n"
#                                 "Stemiot Innovations"
#                             )
#                             html_message = (
#                                 f"<p>Dear {transaction.name},</p>"
#                                 f"<p>Thank you for your payment of {transaction.amount}.</p>"
#                                 f"<p>Your receipt number is <strong>{transaction.mpesa_receipt_number}</strong>.</p>"
#                                 f"<p>Should you have any questions, please feel free to reach us at:</p>"
#                                 f"<p><strong>Phone:</strong> 0115598800</p>"
#                                 f"<p>Powered by <a href='https://stemiotsoftwares.onrender.com/' target='_blank'>Stemiot Innovations</a></p>"
#                                 f"<p>Best regards,<br>Stemiot Innovations</p>"
#                             )
#                             send_mail(
#                                 subject,
#                                 message,
#                                 'engineerotienoduor14@gmail.com',
#                                 [transaction.email],
#                                 fail_silently=False,
#                                 html_message=html_message,
#                             )
#                             print("Payment receipt email sent successfully.")
#
#                     elif result_code == 1:
#                         transaction.status = "Failed"
#                         transaction.description = result_desc
#                         transaction.save()
#                         print(f"Transaction {transaction_id} marked as failed: {result_desc}")
#
#                     elif result_code == 1032:
#                         transaction.status = "Cancelled"
#                         transaction.description = "Transaction cancelled by the user"
#                         transaction.save()
#                         print(f"Transaction {transaction_id} marked as cancelled.")
#
#             return JsonResponse({"message": "Callback received and processed"}, status=200)
#
#         except Exception as e:
#             print(f"Error processing callback: {e}")
#             return JsonResponse({"error": "An error occurred while processing the callback"}, status=500)
#
#     return JsonResponse({"error": "Invalid request method"}, status=400)

def pay(request):
    return render(request,'pay.html')



def payment_success(request):
    return render(request, 'payment_success.html')


def payment_failed(request):
    return render(request, 'payment_failed.html')


def payment_cancelled(request):
    return render(request, 'payment_cancelled.html')


def view_payments(request):
    search_query = request.GET.get('q', '')
    page_number = request.GET.get('page', 1)

    payments = Transaction.objects.filter(
        phone_number__icontains=search_query
    ) | Transaction.objects.filter(
        transaction_id__icontains=search_query
    ) | Transaction.objects.filter(
        name__icontains=search_query
    ) | Transaction.objects.filter(
        mpesa_receipt_number__icontains=search_query
    )

    paginator = Paginator(payments, 10)
    page_obj = paginator.get_page(page_number)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        payments_list = [
            {
                'id': payment.id,
                'transaction_id': payment.transaction_id,
                'name': payment.name,
                'phone_number': payment.phone_number,
                'amount': str(payment.amount),
                'status': payment.status,
                'mpesa_receipt_number': payment.mpesa_receipt_number,
                'transaction_date': payment.transaction_date.strftime(
                    "%Y-%m-%d %H:%M:%S") if payment.transaction_date else "N/A",
                'email': payment.email,
            }
            for payment in page_obj
        ]
        return JsonResponse({
            'payments': payments_list,
            'has_next': page_obj.has_next(),
            'has_previous': page_obj.has_previous(),
            'current_page': page_obj.number,
            'total_pages': paginator.num_pages,
        })

    return render(request, 'view_payments.html', {'page_obj': page_obj})



def blog_list(request):
    blogs = Blog.objects.all().order_by('-filled_at')
    if request.method == "POST":
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('blog_list')
    else:
        form = BlogForm()
    return render(request, 'blogs.html', {'blogs': blogs, 'form': form})



def blog_detail(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    comments = blog.comments.all()
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.blog = blog
            comment.save()
            return redirect('blog_detail', blog_id=blog.id)
    else:
        form = CommentForm()
    return render(request, 'blog_detail.html', {'blog': blog, 'comments': comments, 'form': form})
















# Register function
# def signup_page(request):
#     if request.method == 'POST':
#         form = RegisterForm(request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, "Registration successful! Please log in.")
#             return redirect('login')
#     else:
#         form = RegisterForm()
#
#
#     return render(request, 'signup.html', {'form': form})
#
#
#
# login function
# Create your views here.

