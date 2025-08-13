from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.db.models import Count, Q
from django.db.models.functions import TruncDate
from django.conf import settings
from django.http import HttpResponse
import os
import pandas as pd

from .models import Recipe
from .forms import RecipeSearchForm, RecipeForm
from .utils import get_chart


# ---------------------------
# Auth & basic pages
# ---------------------------

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
                return redirect('recipes:home')
        else:
            error_message = 'Ooops... something went wrong.'

    form.fields['password'].widget.attrs.update({'id': 'password'})
    return render(request, 'auth/login.html', {'form': form, 'error_message': error_message})


def logout_view(request):
    logout(request)
    return redirect('logout_success')


def logout_success(request):
    return render(request, 'auth/success.html')


def welcome(request):
    return render(request, 'welcome.html')


@login_required(login_url='/login/')
def home(request):
    return render(request, 'recipes/home.html')


def about(request):
    return render(request, 'recipes/about.html')


def staticfiles_list(request):
    static_root = settings.STATIC_ROOT
    files_list = []
    for root, dirs, files in os.walk(static_root):
        for file in files:
            rel_dir = os.path.relpath(root, static_root)
            rel_file = os.path.join(rel_dir, file)
            files_list.append(rel_file)
    files_html = "<br>".join(files_list)
    return HttpResponse(f"<h1>Static Files in {static_root}</h1><p>{files_html}</p>")


# ---------------------------
# Search
# ---------------------------

def search_recipes(request):
    form = RecipeSearchForm(request.GET or None)
    recipes = None
    chart = None

    if form.is_valid():
        name = form.cleaned_data.get('name')
        ingredient_name = form.cleaned_data.get('ingredient')
        max_time = form.cleaned_data.get('max_cooking_time')
        difficulty = form.cleaned_data.get('difficulty')
        chart_type = form.cleaned_data.get('chart_type')

        qs = Recipe.objects.all()

        if name:
            qs = qs.filter(name__icontains=name)
        if ingredient_name:
            qs = qs.filter(
                recipe_ingredients__ingredient__name__icontains=ingredient_name
            ).distinct()
        if max_time is not None:
            qs = qs.filter(cooking_time__lte=max_time)
        if difficulty:
            qs = qs.filter(difficulty__iexact=difficulty)

        if qs.exists():
            recipes = qs

            category_data = qs.values('difficulty').annotate(count=Count('id')).order_by('difficulty')
            category_df = pd.DataFrame(list(category_data))
            category_df.rename(columns={'difficulty': 'category'}, inplace=True)

            date_data = qs.annotate(date_added=TruncDate('created')).values('date_added').annotate(count=Count('id')).order_by('date_added')
            date_df = pd.DataFrame(list(date_data))

            if chart_type in ['bar', 'pie']:
                chart = get_chart(chart_type, category_df, labels=category_df['category'].tolist())
            elif chart_type == 'line' and not date_df.empty:
                chart = get_chart(chart_type, date_df)

    context = {'form': form, 'recipes': recipes, 'chart': chart}
    return render(request, 'recipes/search_results.html', context)


# ---------------------------
# Recipe CRUD
# ---------------------------

class RecipeListView(ListView):
    model = Recipe
    template_name = 'recipes/home.html'
    context_object_name = 'recipes'
    paginate_by = 10


class RecipeDetailView(DetailView):
    model = Recipe
    template_name = 'recipes/detail.html'
    context_object_name = 'recipe'  # so templates can use {{ recipe.pic.url }}


class RecipeCreateView(LoginRequiredMixin, CreateView):
    model = Recipe
    form_class = RecipeForm
    template_name = 'recipes/recipe_form.html'
    success_url = reverse_lazy('recipes:list')
    login_url = '/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recipe'] = None  # prevents preview crash on create
        return context


class RecipeUpdateView(LoginRequiredMixin, UpdateView):
    model = Recipe
    form_class = RecipeForm
    template_name = 'recipes/recipe_form.html'
    success_url = reverse_lazy('recipes:list')
    context_object_name = 'recipe'
    login_url = '/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recipe'] = self.object  # for preview on edit
        return context


class RecipeDeleteView(LoginRequiredMixin, DeleteView):
    model = Recipe
    template_name = 'recipes/recipe_confirm_delete.html'
    success_url = reverse_lazy('recipes:list')
    login_url = '/login/'
