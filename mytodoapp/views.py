from django.shortcuts import render, reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Todo
# Create your views here.

@login_required
def index(request):
    """Return the index page.
    The todo list is populated later with a call to `get_all`"""
    return render(request, "mytodoapp/index.html")

@login_required
def add(request):
    """Add a new todo to the current user"""
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
