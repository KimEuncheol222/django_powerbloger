from django.shortcuts import render

# Create your views here.
def login(request):
    return render(request, 'registration/login.html')

def signup(request):
    return render(request, 'registration/signup.html')

def board_client(request):
    return render(request, 'blog_app/board_client.html')

def board_admin(request):
    return render(request, 'blog_app/board_admin.html')

def post(request):
    return render(request, 'blog_app/post.html')

def write(request):
    return render(request, 'blog_app/write.html')