from django.contrib.auth.models import User
from django.contrib import auth
from django.shortcuts import render, redirect, get_object_or_404
from .models import CustomUser, BlogPost
from .serializers import BlogPostSerializer
from .forms import BlogPostForm
from django.db.models import Q
from .forms import SearchForm
from django.conf import settings
from bs4 import BeautifulSoup

# 로그인 views
def login_view(request):
    # POST요청이 들어온다면
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(request, username=username, password=password)
        # 해당 유저가 존재한다면
        if user is not None:
            auth.login(request, user)
            return redirect('board')
        else:
            return render(request, 'registration/login.html', {'error':'ID와 password를 확인해주세요.'})
        
    return render(request, 'registration/login.html')

# 로그아웃 views
def logout_view(request):
    # 로그아웃 성공시 로그인 화면으로
    if request.method == 'POST':
        auth.logout(request)
        return redirect('login')
    return render(request, 'registration/login.html')

# 회원가입 views

def signup_view(request):
    if request.method == 'POST':
        if request.POST['password'] == request.POST['password_confirm']:
            username = request.POST['username']
            password = request.POST['password']
            password_confirm = request.POST['password_confirm']
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            email = request.POST['email']
            phone_number = request.POST['phone_number']

            try:
                user = CustomUser.objects.create_user(username=username, email=email, password=password)
                user.last_name = last_name
                user.first_name = first_name
                user.phone_number = phone_number
                user.save()
                return redirect('login')
            except Exception:
                return render(request, 'registration/signup.html', {'signup_error': '입력이 잘못됐습니다.'})
    return render(request, 'registration/signup.html')

def find_password(request):
    if request.method == 'POST':
        username = request.POST['username']
        phone_number = request.POST['phone_number']
        try:
            user = CustomUser.objects.get(username=username, phone_number=phone_number)
            return redirect('new_password', username=username)
        except CustomUser.DoesNotExist:
            # 사용자가 존재하지 않는 경우에 대한 처리
            return render(request, 'registration/find_password.html', {'new_error':'ID와 전화번호를 확인해주세요.'})
    return render(request, 'registration/find_password.html')

def new_password(request, username):
    user = CustomUser.objects.get(username=username)
    if request.method == 'POST':
        password = request.POST['password']
        password_confirm = request.POST['password_confirm']
        if password == password_confirm:
            user.set_password(password)
            user.save()
            return redirect('login')  # 비밀번호 재설정 후 로그인 페이지로 이동
        else:
            # 비밀번호가 일치하지 않을 때의 처리
            return render(request, 'registration/new_password.html', {'password_error':'비밀번호가 일치하지 않습니다.'})
    return render(request, 'registration/new_password.html')

def board(request):
    recent_posts = BlogPost.objects.order_by('-created_at')[:3]  # 최근 게시물 3개 가져오기
    context = {'recent_posts': recent_posts}
    return render(request, 'blog_app/board.html', context)

def post(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id)  # 해당 포스트를 가져오거나 404 에러 반환

    if request.method == 'POST':
        
        # 요청에 삭제가 포함된경우
        if 'delete-button' in request.POST:
            post.delete()
            return redirect('board')
    
    # 조회수 증가 및 db에 저장
    post.views += 1 
    post.save() 

    # 이전/다음 게시물 가져옴
    previous_post = BlogPost.objects.filter(id__lt=post.id, is_draft=False).order_by('-id').first()
    next_post = BlogPost.objects.filter(id__gt=post.id, is_draft=False).order_by('id').first()

    # 같은 주제인 게시물들 중 최신 글 가져옴
    recommended_posts = BlogPost.objects.filter(topic=post.topic, is_draft=False).exclude(id=post.id).order_by('-created_at')[:2]

    # 게시물 내용에서 첫번째 이미지(썸네일) 태그 추출
    for recommended_post in recommended_posts:
        soup = BeautifulSoup(recommended_post.content, 'html.parser')
        image_tag = soup.find('img')
        recommended_post.image_tag = str(image_tag) if image_tag else ''

    context = {
        'post': post,
        'previous_post': previous_post,
        'next_post': next_post,
        'recommended_posts': recommended_posts,
        'MEDIA_URL': settings.MEDIA_URL,
    }

    return render(request, 'blog_app/post.html', context)

def write(request):
    if request.method == 'POST':
        write_form = BlogPostForm(request.POST)
        if write_form.is_valid():
            blog_post = write_form.save(commit=False)
            blog_post.author = request.user
            blog_post.is_draft = False
            blog_post.save()
            return redirect('post', post_id=blog_post.id)   
    else:
        write_form = BlogPostForm(initial={'is_draft': False})

    return render(request, 'blog_app/write.html', {'write_form': write_form})



def find_password(request):
    return render(request, 'registration/find_password.html')

def new_password(request):
    return render(request, 'registration/new_password.html')


# 작성된 게시글 키워드 검색기능
def search_view(request):
    if request.method == 'GET':
        form = SearchForm(request.GET)
        if form.is_valid():
            keyword = form.cleaned_data['keyword']
            # 제목 또는 본문 내용에 키워드를 포함하는 게시글을 검색합니다.
            results = BlogPost.objects.filter(Q(title__icontains=keyword) | Q(content__icontains=keyword))
            return render(request, 'blog_app/search.html', {'results': results})
    return render(request, 'blog_app/search.html', {'results': []})

def filter_daily(request):
    daily_posts = BlogPost.objects.filter(topic__name='일상')[:3]
    context = {'daily_posts': daily_posts}
    return render(request, 'blog_app/board.html', context)

def filter_cook(request):
    cook_posts = BlogPost.objects.filter(topic__name='요리')[:3]
    context = {'daily_posts': cook_posts}
    return render(request, 'blog_app/board.html', context)

def filter_travel(request):
    travel_posts = BlogPost.objects.filter(topic__name='여행')[:3]
    context = {'daily_posts': travel_posts}
    return render(request, 'blog_app/board.html', context)

def filter_movie(request):
    movie_posts = BlogPost.objects.filter(topic__name='영화')[:3]
    context = {'daily_posts': movie_posts}
    return render(request, 'blog_app/board.html', context)

def filter_it(request):
    it_posts = BlogPost.objects.filter(topic__name='IT')[:3]
    context = {'daily_posts': it_posts}
    return render(request, 'blog_app/board.html', context)