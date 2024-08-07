from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='/login/')
def Recipes(request):
    if request.method == "POST":
       
       data = request.POST

       image = request.FILES.get('image')
       recipe_name = data.get('recipe_name')
       method = data.get('method')

       Recipe.objects.create(
           recipe_name = recipe_name,
           method= method,
           image=image,
     )
       return redirect('/Recipes/')
    
    queryset = Recipe.objects.all()
      
    if request.GET.get('Search'):
          queryset = queryset.filter(recipe_name__icontains= request.GET.get('Search'))

    context = {'Recipe': queryset}


    return render(request, 'Recipes.html', context)

def update_recipe(request, id):
       queryset= Recipe.objects.get(id = id)
       if request.method =="POST":
            data = request.POST
            image = request.FILES.get('image')
            recipe_name = data.get('recipe_name')
            method = data.get('method')

            queryset.recipe_name=recipe_name
            queryset.method=method
            
            if image:
                  queryset.image=image

            queryset.save()
            return redirect('/Recipes/')
            

       context = {'Recipe': queryset}
       return render(request, 'update_recipe.html', context)

def delete_recipe(request, id):
      queryset= Recipe.objects.get(id = id)
      queryset.delete()
      return redirect('/Recipes/')

def login_page(request):
      if request.method == "POST":
          username = request.POST.get('username')
          password = request.POST.get('password')
          
          if not User.objects.filter(username = username).exists():
                messages.info(request, "Invalid Username")
                return redirect('/login/')
                
          user = authenticate(username = username, password = password)
          if user is None:
                messages.info(request, "Invalid Username or Password")
                return redirect('/login/')
          else:
                login(request, user)
                return redirect('/Recipes/')

      return render(request , 'login.html')
def logout_page(request):
     logout(request)
     return redirect('/login/')
def register(request):
     if request.method == "POST":
          first_name = request.POST.get('first_name')
          last_name = request.POST.get('last_name')
          username = request.POST.get('username')
          password = request.POST.get('password')
         
          user = User.objects.filter(username = username)

          if user.exists():
                messages.info(request, "User name already taken")
                return redirect('/register/')
          
          user = User.objects.create(
              first_name=first_name,
              last_name=last_name,
              username=username
             )
          user.set_password(password)
          user.save()
          messages.info(request, "User name created successfuly")

          return redirect('/register/')
       
     return render(request , 'register.html')