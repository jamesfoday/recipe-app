from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from .models import Recipe
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required

def login_view(request):
    error_message = None
    form = AuthenticationForm()

    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('sales:records')
        else:
            error_message = 'Ooops... something went wrong.'

    # Add id attribute for password toggle JS
    form.fields['password'].widget.attrs.update({'id': 'password'})

    context = {
        'form': form,
        'error_message': error_message,
    }
    return render(request, 'auth/login.html', context)


@login_required(login_url='/login/')
def home(request):
    # You can add logic to fetch recipes if needed
    return render(request, 'recipes/home.html')


def logout_view(request):
    logout(request)
    return redirect('logout_success')


def logout_success(request):
    return render(request, 'auth/success.html')


def welcome(request):
    return render(request, 'welcome.html')


class RecipeListView(ListView):
    model = Recipe
    template_name = 'recipes/home.html'


class RecipeDetailView(DetailView):
    model = Recipe
    template_name = 'recipes/detail.html'
