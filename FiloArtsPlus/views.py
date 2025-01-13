from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

def gallery(request):
    return render(request, 'gallery.html')

def blogs(request):
    return render(request, 'blogs.html')

# Create your views here.
