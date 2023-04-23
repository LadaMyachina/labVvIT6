

# Create your views here.
from .models import Article
from django.shortcuts import render
from django.http import Http404
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm

def archive(request):
    return render(request, 'archive.html', {"posts": Article.objects.all()})


def get_article(request, article_id):
    try:
        post = Article.objects.get(id=article_id)
        return render(request, 'article.html', {"post": post})
    except Article.DoesNotExist:
        raise Http404

def create_post(request):
    #if not request.user.is_anonymous():
    if request.user.is_authenticated:
        if request.method == "POST":
            # обработать данные формы, если метод POST
            form = {
                'text': request.POST["text"], 'title': request.POST["title"]
            }
            # в словаре form будет храниться информация, введенная пользователем
            if form["text"] and form["title"] and not Article.objects.filter(title=form["title"]).exists():
                # если поля заполнены без ошибок
                Article.objects.create(text=form["text"], title=form["title"], author=request.user)
                return redirect('get_article', article_id=article.id)
            # перейти на страницу поста
            else:
                # если введенные данные некорректны
                if Article.objects.filter(title=form["title"]).exists() and not (form["text"] ):
                    form["errors"]= u"Название статьи не уникально!\nНе все поля заполнены!"
                elif Article.objects.filter(title=form["title"]).exists():
                    form["errors"]=u"Название статьи не уникально!"
                else:
                    form["errors"]=u"Не все поля заполнены!"
                return render(request, 'create_post.html', {'form': form})
        else:
            # просто вернуть страницу с формой, если метод GET
            return render(request, 'create_post.html', {})

    else:
        raise Http404

'''def registration(request):
    if request.method == "POST":
        form = {
            'username': request.POST["username"],
            'mail': request.POST["mail"],
            'password': request.POST["password"]
        }
        art = None
        try:
            art = User.objects.get(username=form["username"])
            art = User.objects.get(email=form["mail"])
            # если юзер существует, то ошибки не произойдет и программа удачно доберется до следующей строчки
            print (u"Такой пользователь уже есть")
        except User.DoesNotExist:
            print (u"Такого пользователя еще нет")
            if form["username"] and form["mail"] and form["password"] and art is None:
                art = User.objects.registration(username=form["username"], email=form["mail"], password=form["password"])
                return redirect(archive)
            else:
                if art is not None:
                    form['errors'] = u"Логин или почта уже заняты"
                else:
                    form['errors'] = u"Не все поля заполнены"
                return render(request, 'registration.html', {'form': form})
    else:
        return render(request, 'registration.html', {})'''


'''def registration(request):
    if request.method == "POST":
        form = {
            'username': request.POST.get("username", ""),
            'email': request.POST.get("email", ""),
            'password': request.POST.get("password", "")
        }
        if not all(form.values()):
            form['errors'] = u"Не все поля заполнены"
            return render(request, 'registration.html', {'form': form})

        try:
            User.objects.get(username=form["username"])
            form['errors'] = u"Логин уже занят"
            return render(request, 'registration.html', {'form': form})
        except User.DoesNotExist:
            pass

        return redirect("user_login")
    else:
        return render(request, 'registration.html', {})'''

def registration(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            # получаем имя пользователя и пароль из формы
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            # выполняем аутентификацию
            user = authenticate(username=username, email=email, password=password)
            login(request, user)
            return redirect("user_login")
    else:
        form = UserCreationForm()
    return render(request, 'registration.html', {'form': form})

"""def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("create_post")
        else:
            return render(request, 'user_login.html', {'error': 'Неверное имя пользователя или пароль'})
    else:
        return render(request, 'user_login.html', {})"""

'''def registration(request):
    if request.method == "POST":
        form = {
            'username': request.POST.get("username", ""),
            'email': request.POST.get("email", ""),
            'password': request.POST.get("password", "")
        }
        if not all(form.values()):
            form['errors'] = u"Не все поля заполнены"
            return render(request, 'registration.html', {'form': form})

        try:
            User.objects.get(username=form["username"])
            form['errors'] = u"Логин уже занят"
            return render(request, 'registration.html', {'form': form})
        except User.DoesNotExist:
            pass

        user = User.objects.create_user(form["username"], form["email"], form["password"])
        user.save()

        return redirect("user_login")
    else:
        return render(request, 'registration.html', {})'''

def user_login(request):
    if request.method == "POST":
        form = {
            'username': request.POST.get("username", ""),
            'password': request.POST.get("password", "")
        }
        if form["username"] and form["password"]:
            user = authenticate(request, username=form["username"], password=form["password"])
            if user is not None:
                login(request, user)
                return redirect('archive')
            else:
                form['errors'] = u"Такой пользователь не зарегистрирован!"
        else:
            form['errors'] = u"Не все поля заполнены"
        return render(request, 'user_login.html', {'form': form})
    else:
        return render(request, 'user_login.html', {})