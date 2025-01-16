from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from FiloArtsPlus.models import Client
from .forms import CustomLoginForm


def index(request):
    return render(request, 'index.html')

def gallery(request):
    return render(request, 'gallery.html')

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

def custom_login_view(request):
    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('clients')  # Redirect to the clients page

            else:
                form.add_error(None, 'Invalid username or password')
    else:
        form = CustomLoginForm()
    return render(request, 'login.html', {'form': form})

# Create your views here.
