from django.shortcuts import render, redirect
from .models import User
from django.contrib import messages
import bcrypt
from belt_app.models import Tree

def index(request):

    return render(request, "index.html")


def register(request):

    errors = User.objects.register_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/")
    password = request.POST['password']
    pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    User.objects.create(first_name = request.POST['first_name'], last_name = request.POST['last_name'],
                        email = request.POST['email'], password=pw_hash, birth_date = request.POST['birth_date'])

    user = User.objects.filter(email = request.POST['email'])
    logged_user = user[0]
    request.session['user_id'] = logged_user.id
    request.session['name'] = logged_user.first_name + " " + logged_user.last_name
    request.session['first_name'] = logged_user.first_name


    return redirect("/dashboard")

def login(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/")
    user = User.objects.filter(email = request.POST['email'])
    if user:
        logged_user = user[0]
        
        if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
            request.session['user_id'] = logged_user.id
            request.session['name'] = logged_user.first_name + " " + logged_user.last_name
            request.session['first_name'] = logged_user.first_name

            return redirect("/dashboard")
        else:
            errors = User.objects.login_validator(request.POST)
            errors['wrong_password'] = "Wrong password!"
            if len(errors) > 0:
                for key, value in errors.items():
                    messages.error(request, value)
            return redirect("/")

def logout(request):
    del request.session['user_id']
    request.session.save()
    return redirect("/")

def my_trees(request, firstname):
    context = {
        "user" : User.objects.get(first_name = firstname),
        # "trees" : Tree.objects.get(user=User.objects.get(first_name = firstname)),
        "trees" : User.objects.get(first_name = firstname).trees.all(),
    }

    return render(request, "my_trees.html", context)

def delete_tree(request, tree_id):
    tree = Tree.objects.get(id=tree_id)
    name = tree.user.first_name
    c = Tree.objects.get(id = tree_id)
    c.delete()
    return redirect(f'/{name}/account')

def show_add_tree(request):
    context = {
        "user" : User.objects.get(id = request.session['user_id']),
    }
    return render(request, "add_tree.html", context)

def add_tree(request):
    errors = Tree.objects.tree_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/new/tree")
    else:
        Tree.objects.create(species = request.POST['species'], user = User.objects.get(id = request.session['user_id']), location = request.POST['location'], reason = request.POST['reason'], date_planted = request.POST['date_planted'])
   

        return redirect("/dashboard")

def tree_details(request, tree_id):
    tree = Tree.objects.get(id=tree_id)
    context = {
        "tree" : Tree.objects.get(id = tree_id),
        'this_user': User.objects.get(id = request.session['user_id']),
    }

    return render(request, "tree_details.html", context)

def edit_tree(request, tree_id):
    tree = Tree.objects.get(id=tree_id)
    context = {
        "tree" : Tree.objects.get(id = tree_id),
        'this_user': User.objects.get(id = request.session['user_id']),
    }

    return render(request, "edit_tree.html", context)

def update_tree(request, tree_id):

    errors = Tree.objects.tree_validator(request.POST)
    tree = Tree.objects.get(id=tree_id)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/new/tree")
    c = Tree.objects.get(id = tree_id)
    if request.POST['species']:
        c.species = request.POST['species']
    if request.POST['location']:
        c.location = request.POST['location']
    if request.POST['reason']:
        c.reason = request.POST['reason']
    if request.POST['date_planted']:
        c.date_planted = request.POST['date_planted']
    c.save()

    return redirect((f'/show/{tree.id}'))




