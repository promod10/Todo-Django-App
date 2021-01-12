from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login as loginUser, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from todo.forms import TodoForm
from todo.models import Todo
from django.contrib.auth.decorators import login_required

# Create your views here.


@login_required(login_url='login')
def home(request):
    if request.user.is_authenticated:
        user = request.user
        form = TodoForm()
        todos = Todo.objects.filter(user=user).order_by('priority')
        return render(request, 'todo/home.html', context={'form': form, 'todos': todos})


def login(request):
    if request.method == 'GET':
        form = AuthenticationForm()
        context = {'form': form}
        return render(request, 'todo/login.html', context=context)
    else:
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                loginUser(request, user)
                return redirect('home')

        else:
            context = {'form': form}
            return render(request, 'todo/login.html', context=context)


def signup(request):
    if request.method == 'GET':
        form = UserCreationForm()
        context = {'form': form}
        return render(request, 'todo/signup.html', context=context)
    else:
        form = UserCreationForm(request.POST)
        context = {'form': form}
        if form.is_valid():
            user = form.save()
            if user is not None:
                return redirect('login')
        else:
            return render(request, 'todo/signup.html', context=context)


@login_required(login_url='login')
def add(request):
    if request.user.is_authenticated:
        user = request.user
    form = TodoForm(request.POST)
    if form.is_valid():
        todo = form.save(commit=False)
        todo.user = user
        todo.save()
        return redirect('home')
    else:
        return render(request, 'todo/home.html', context={'form': form})


def signout(request):
    logout(request)
    return redirect('login')


def delete(request, id):
    Todo.objects.get(pk=id).delete()
    return redirect('home')


def change(request, id, status):
    todo = Todo.objects.get(pk=id)
    todo.status = status
    todo.save()
    return redirect('home')
