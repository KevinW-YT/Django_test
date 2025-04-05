from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from .models import ToDoItem
from django.shortcuts import get_object_or_404



# Create your views here.
def home(request):
    exercise_tasks = ToDoItem.objects.filter(category=ToDoItem.EXERCISE)
    stretching_tasks = ToDoItem.objects.filter(category=ToDoItem.STRETCHING)
    cardio_tasks = ToDoItem.objects.filter(category=ToDoItem.CARDIO)
    return render(request, 'myapp/home.html', {
        'exercise_tasks': exercise_tasks,
        'stretching_tasks': stretching_tasks,
        'cardio_tasks': cardio_tasks
    })  # Make sure to create this template

def login(request):
    return render(request, 'myapp/login.html')

def register(request):
    return render(request, 'myapp/register.html')

def task_list(request):
    category = request.GET.get('category', '')  # Check if category is passed via GET params
    tasks = ToDoItem.objects.all()  # Get all tasks by default

    # If a category is provided, filter tasks based on the category
    if category:
        tasks = tasks.filter(category=category)
    return render(request, 'task_list.html', {'tasks': tasks, 'category': category or 'ALL'})

# def exercise_list(request):
#     exercises = ToDoItem.objects.filter(category=ToDoItem.EXERCISE, completed=False)  # Exclude completed tasks
#     return render(request, 'exercise_list.html', {'tasks': exercises})

# def add_exercise_task(request):
#     if request.method == 'POST':
#         title = request.POST.get('title')  # Get the task title from the form
#         if title:
#             ToDoItem.objects.create(title=title, category=ToDoItem.EXERCISE)  # Create a new task
#         return redirect('exercise_list')  # Redirect back to the exercise list

def category_task_list(request, category):
    tasks = ToDoItem.objects.filter(category=category, completed=False)  # Filter by category and exclude completed
    return render(request, 'task_list.html', {'tasks': tasks, 'category': category})

def add_task(request, category):
    if request.method == 'POST':
        title = request.POST.get('title')  # Get the task title from the form
        if title:
            ToDoItem.objects.create(title=title, category=category)  # Create a new task for the category
        return redirect('category_task_list', category=category)  # Redirect back to the category list

def mark_task_complete(request, category, task_id):
    task = get_object_or_404(ToDoItem, id=task_id, category=category)
    task.completed = True
    task.save()
    return redirect('category_task_list', category=category)  # Redirect back to the category list

def stretching_list(request):
    stretching = ToDoItem.objects.filter(category=ToDoItem.STRETCHING)
    return render(request, 'task_list.html', {'tasks': stretching, 'category': ToDoItem.STRETCHING})

def exercise_list(request):
    exercise = ToDoItem.objects.filter(category=ToDoItem.EXERCISE)
    return render(request, 'task_list.html', {'tasks': exercise, 'category': ToDoItem.EXERCISE})

def cardio_list(request):
    cardio = ToDoItem.objects.filter(category=ToDoItem.CARDIO)
    return render(request, 'task_list.html', {'tasks': cardio, 'category': ToDoItem.CARDIO})