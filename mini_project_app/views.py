# get_object_or_404 calls get on a given model and the object which are also the arguments
# If none of them exists it calls 404 helping to write less code
# Render is a function that combines a given template with a given context dictionary
# Returns an HTTPResponse object with that rendered text
# Context is an optional argument of render, which by default is an empty dictionary
from django.shortcuts import render, get_object_or_404
from .models import Todo
from django.http import HttpResponseRedirect
from django.urls import reverse


# The view function is provided with the request obj that contains a lot of data
def index(request):
    # We check if the method of the request is POST
    if request.method == "POST":
        # This corresponds with the name of the input tag that we store in a variable
        text = request.POST["text"]
        # We create an object instance using the todo class
        todo = Todo()
        todo.user = request.user
        todo.text = text
        # Method that saves it to the database
        todo.save()

    # The query set returned by Todo.objects.all() returns the whole database table
    # That is why we can refine the QuerySet with filter - reuturns obj that match the given lookup params
    # or with exclude - returns obj that do NOT match the given lookup params
    # Basically we return the non-completed todos
    todos = Todo.objects.filter(status=False)

    context = {
            'todos': todos
    }
    return render(request, 'mini_project_app/index.html', context)


def change_status(request):
    # We get the pk from the request object which is a hidden field, pk meaning primary key
    pk = request.POST["pk"]
    todo = get_object_or_404(Todo, pk=pk)
    if "checked" in request.POST:
        todo.status = True
    else:
        todo.status = False
    todo.save()
    # We return the user to the index view passing in the name of the project and the name of the path fc in the urls.py
    # Reverse imports the name of all the URLconf files and examines the name of each view
    return HttpResponseRedirect(reverse('mini_project_app:index'))

# View fc for this route: path('completed_todos', views.completed_todos, name='completed_todos')
def completed_todos(request):
    todos = Todo.objects.filter(status=True)
    context = {
            'todos': todos
            }
    return render(request, 'mini_project_app/completed_todos.html', context)

# View fc for this route: path('delete_todo', views.delete_todo, name="delete_todo")
def delete_todo(request):
    # print(request.META)
    pk = request.POST["pk"]
    todo = get_object_or_404(Todo, pk = pk)
    todo.delete()
    # request.META prints: 'HTTP_REFERER': 'http://127.0.0.1:8000/todo/'
    # split prints ['http:', '', '127.0.0.1:8000', 'todo', '']
    # [-2] is equivalent with [3] and prints todo
    # We do this because deletion should be possible from two different routes so we check on which
    # route we are
    if request.META['HTTP_REFERER'].split('/')[-2] == 'todo':
        return HttpResponseRedirect(reverse('mini_project_app:index'))
    else:
        return HttpResponseRedirect(reverse('mini_project_app:completed_todos'))
