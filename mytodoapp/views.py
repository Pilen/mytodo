from django.shortcuts import render, reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, Http404
from django.contrib.auth.models import User
from django.contrib.auth import login as _login, logout as _logout, authenticate as _authenticate
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Todo


def index(request):
    """Return the index page.
    The todo list is populated later with a call to `get_all`"""
    if request.user.is_authenticated:
        return render(request, "mytodoapp/index.html")
    else:
        return HttpResponseRedirect(reverse("login"))


################################################################################
#                                     API                                      #
################################################################################

@login_required
def add(request):
    """Add a new todo to the current user"""
    if not "title" in request.POST or not request.POST["title"]:
        return JsonResponse({"message": "Missing title"}, status=400)
    todo = Todo.objects.create(title=request.POST["title"],
                               description=request.POST["description"],
                               created_date=timezone.now(),
                               author=request.user)
    return JsonResponse(todo.to_dict())

@login_required
def get_all(request):
    """Get all todos for the current user"""
    todos = request.user.todo_set.order_by("created_date")
    json = [todo.to_dict() for todo in todos]
    return JsonResponse(json, safe=False)

@login_required
def change(request):
    """Change the closed/open status"""
    todo = Todo.objects.get(id=request.POST["id"])
    todo.closed = request.POST["closed"] == "true"
    todo.save()
    return JsonResponse(todo.to_dict())

@login_required
def delete(request):
    """Delete a todo"""
    todo = Todo.objects.get(id=request.POST["id"])
    id = todo.id
    todo.delete()
    return JsonResponse({"deleted": id})



################################################################################
#                                 Registration                                 #
################################################################################
# TODO: This should be placed in a proper user handling app

def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = _authenticate(request, username=username, password=password)
        if user is not None:
            _login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "registration/login.html")

def register(request):
    try:
        username = request.POST["username"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]
        if not username or not password1 or password1 != password2:
            return HttpResponseRedirect(reverse("login"))
        user = User.objects.create_user(username, "", password1)
        _login(request, user)
        return HttpResponseRedirect(reverse("index"))
    except:
        return HttpResponseRedirect(reverse("login"))


def logout(request):
    _logout(request)
    return HttpResponseRedirect(reverse("login"))
