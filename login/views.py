import hashlib
from login import froms, models
from django.shortcuts import render, redirect


# Create your views here.
def hash_code(s, salt='mysite_3'):# 加点盐
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())  # update方法只接收bytes类型
    return h.hexdigest()


def index(request):
    return render(request, 'login/index.html')


def login(request):
    if request.session.get('is_login', None):
        return redirect('/index/')
    if request.method == 'POST':
        login_form = froms.UserForm(request.POST)
        message = '请检查你填的信息'
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            try:
                user = models.Users.objects.get(name=username)
                if user.password == hash_code(password):
                    request.session['is_login'] = True
                    request.session['user_id'] = user.id
                    request.session['user_name'] = user.name
                    return redirect('/index/')
                message = '密码错误'
            except:
                message = '用户不存在'
        return render(request, 'login/login.html', locals())
    login_form = froms.UserForm()
    return render(request, 'login/login.html', locals())


def register(request):
    if request.session.get('is_login', None):
        return redirect('/index/')
    if request.method == 'POST':
        register_form = froms.RegisterForm(request.POST)
        message = '请检查你输入的信息'
        if register_form.is_valid():
            username = register_form.cleaned_data['username']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            email = register_form.cleaned_data['email']
            sex = register_form.cleaned_data['sex']
            if password1 != password2:
                message = '两次输入的密码不相同'
                return render(request, 'login/register.html', locals())
            else:
                same_user_name = models.Users.objects.filter(name=username)
                if same_user_name:
                    message = '用户已被注册'
                    return render(request, 'login/register.html', locals())

                same_user_email = models.Users.objects.filter(email=email)
                if same_user_email:
                    message = '邮箱已被注册'
                    return render(request, 'login/register.html', locals())

                new_user = models.Users()
                new_user.name = username
                new_user.password = hash_code(password1)
                new_user.email = email
                new_user.sex = sex
                new_user.save()
                return render(request, 'login/register.html', locals())

    register_form = froms.RegisterForm()
    return render(request, 'login/register.html', locals())


def logout(request):
    if not request.session.get('in_login', None):
        return redirect('/index/')
    request.session.flush()
    return redirect('/index/')