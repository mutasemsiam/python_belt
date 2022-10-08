from django.shortcuts import render, redirect
from .models import User, Tree
from django.contrib import messages

def show_main(request):
    if 'user_id' not in request.session:
        
        return redirect("/") 
    context = {
        "all_the_trees": Tree.objects.all(),
        'this_user': User.objects.get(id = request.session['user_id']),
        
    } 

    return render(request,"show_all.html", context)
