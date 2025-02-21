from django.shortcuts import render, redirect, get_object_or_404
from .models import Task
from .forms import TaskForm

def task_list(request):
    search_query = request.GET.get('search', '')  # Get the search query from the form
    tasks = Task.objects.all()  # Get all tasks

    if search_query:
        tasks = tasks.filter(title__icontains=search_query)  # Filter tasks by title (case-insensitive)

    return render(request, 'tasks/task_list.html', {'tasks': tasks, 'search_query': search_query})  # ✅ Ensure this return statement exists

def task_create(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('task_list')  # Redirect to task list after saving
    else:
        form = TaskForm()
    
    return render(request, 'tasks/task_form.html', {'form': form})

def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_list')  # Redirect to task list after update
    else:
        form = TaskForm(instance=task)
    
    return render(request, 'tasks/task_form.html', {'form': form})

def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == "POST":
        task.delete()
        return redirect('task_list')  # Redirect after deletion
    
    return render(request, 'tasks/task_confirm_delete.html', {'task': task})
