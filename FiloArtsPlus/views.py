from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from FiloArtsPlus.models import Client, Drawing, User1
from .forms import CustomLoginForm
from .forms import RegisterForm,CustomLoginForm




def index(request):
    return render(request, 'index.html')

def gallery(request):
    drawings = Drawing.objects.all()
    return render(request, 'gallery.html', {'drawings':drawings})

def blogs(request):
    return render(request, 'blogs.html')


# Function for fetching and plotting the clients details on the database
def client_data(request):
    if request.method == 'POST':
        client_name = request.POST['client_name']
        client_email = request.POST['client_email']
        client_message = request.POST['client_message']

        client = Client(
            client_name= client_name,
            client_email= client_email,
            client_message= client_message

        )

        client.save()
        return redirect('/')


# Function for the clients table

@login_required(login_url='login')
def view_clients(request):
    clients = Client.objects.all()
    return render(request, 'clients.html', {'clients':clients})





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



# Create your views here.
