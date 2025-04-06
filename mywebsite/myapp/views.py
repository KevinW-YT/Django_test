from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from .models import ToDoItem
from django.shortcuts import get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from .utils import get_tips_from_gemini_ai
from django.http import JsonResponse
from .models import ToDoItem
from .utils import get_tips_from_gemini_ai

# Create your views here.
def home(request):
    categories = ['exercise', 'cardio', 'stretching']
    tasks_by_category = {
        category: ToDoItem.objects.filter(category=category, completed=False)
        for category in categories
    }

    # Combine all tasks into a single list to send to the AI
    all_tasks = ToDoItem.objects.filter(completed=False)
    tips = get_tips_from_gemini_ai(all_tasks)  # Fetch tips from Gemini AI

    return render(request, 'home.html', {'tasks_by_category': tasks_by_category, 'tips': tips})

def get_tips(request):
    if not request.user.is_authenticated:
        return JsonResponse({"tips": ["Please log in to get personalized tips."]})

    tasks = ToDoItem.objects.filter(user=request.user, completed=False)  # Filter tasks by user
    tips = get_tips_from_gemini_ai(tasks)  # Fetch tips from Gemini AI
    return JsonResponse({"tips": tips})

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Signup successful! Welcome, {}.".format(user.username))
            return redirect('home')
        else:
            messages.error(request, "Signup failed. Please correct the errors below.")
    else:
        form = UserCreationForm()
    return render(request, 'myapp/signup.html', {'form': form})

def task_list(request):
    category = request.GET.get('category', '')  # Check if category is passed via GET params
    tasks = ToDoItem.objects.all()  # Get all tasks by default

    # If a category is provided, filter tasks based on the category
    if category:
        tasks = tasks.filter(category=category)
    return render(request, 'task_list.html', {'tasks': tasks, 'category': category or 'ALL'})

def category_task_list(request, category):
    tasks = ToDoItem.objects.filter(category=category, completed=False)  # Filter by category and exclude completed
    return render(request, 'task_list.html', {'tasks': tasks, 'category': category})

def add_task(request, category):
    if request.method == 'POST':
        title = request.POST.get('title')  # Get the task title from the form
        if title:
            ToDoItem.objects.create(title=title, category=category, user=request.user)  # Create a new task for the category
        return redirect('home')  # Redirect back to the home page


@login_required
def mark_task_complete(request, category, task_id):
    task = get_object_or_404(ToDoItem, id=task_id, category=category)
    if not task.completed:  # Only award points if the task is not already completed
        task.completed = True
        task.save()
        # Award points to the logged-in user
        request.user.profile.points += 10  # Add 10 points (or any value you choose)
        request.user.profile.save()
    return redirect('home')  # Redirect back to the home page


def stretching_list(request):
    stretching = ToDoItem.objects.filter(category=ToDoItem.STRETCHING)
    return render(request, 'task_list.html', {'tasks': stretching, 'category': ToDoItem.STRETCHING})

def exercise_list(request):
    exercise = ToDoItem.objects.filter(category=ToDoItem.EXERCISE)
    return render(request, 'task_list.html', {'tasks': exercise, 'category': ToDoItem.EXERCISE})

def cardio_list(request):
    cardio = ToDoItem.objects.filter(category=ToDoItem.CARDIO)
    return render(request, 'task_list.html', {'tasks': cardio, 'category': ToDoItem.CARDIO})

# def mark_task_complete(request, category, task_id):
#     task = get_object_or_404(ToDoItem, id=task_id, category=category)
#     task.completed = True
#     task.save()
#     return redirect('home')  # Redirect back to the category list


# def exercise_list(request):
#     exercises = ToDoItem.objects.filter(category=ToDoItem.EXERCISE, completed=False)  # Exclude completed tasks
#     return render(request, 'exercise_list.html', {'tasks': exercises})

# def add_exercise_task(request):
#     if request.method == 'POST':
#         title = request.POST.get('title')  # Get the task title from the form
#         if title:
#             ToDoItem.objects.create(title=title, category=ToDoItem.EXERCISE)  # Create a new task
#         return redirect('exercise_list')  # Redirect back to the exercise list