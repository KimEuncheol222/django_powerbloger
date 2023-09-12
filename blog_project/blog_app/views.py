from django.contrib.auth.models import User
from django.contrib import auth
from django.shortcuts import render, redirect
from .models import User

# 로그인 views
def login_view(request):
    # POST요청이 들어온다면
    if request.mothod == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username=username, password=password)
        # 해당 유저가 존재한다면
        if user is not None:
            auth.login(request, user)
            return redirect('user:home')
        else:
            return render(request, 'myapp/signin.html', {'error':'ID와 password를 확인해주세요.'})
        
    return render(request, 'blog_app/login.html')

# 로그아웃 views
def logout_view(request):
    # 로그아웃 성공시 로그인 화면으로
    if request.method == 'POST':
        auth.logout(request)
        return redirect('user:login')
    return render(request, 'blog_app/login.html')

# 회원가입 views
def signup_view(request):
    # POST요청이 들어온다면
    if request.method == 'POST':
        if request.POST['password'] == request.POST['password_confirm']:
            username = request.POST['username'],
            password = request.POST['password'],
            password_confirm = request.POST['password_confirm'],
            firstname = request.POST['first_name'],
            lastname = request.POST['last_name'],
            email = request.POST['email'],
            phone_number = request.POST['phone_number']

            user = User.objects.create_user(username, email, password)
            user.password_confirm = password_confirm
            user.lastname = lastname
            user.firstname = firstname
            user.phone_number = phone_number
            user.save()

            # 회원가입시 자동 로그인
            # auth.login(request, user)
            # 직접 로그인 시키기
        return redirect('user:login')

    return render(request, 'blog_app/signup.html')

def board_client(request):
    return render(request, 'blog_app/board_client.html')

def board_admin(request):
    return render(request, 'blog_app/board_admin.html')

def post(request):
    return render(request, 'blog_app/post.html')

def write(request):
    return render(request, 'blog_app/write.html')