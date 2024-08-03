from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import UserRegisterForm, ProfileForm, ProjectForm, TaskForm, CommentForm, MessageForm, SearchForm, TaskFilterForm
from .models import Project, Task, Comment, Profile, Message, User
from django.contrib.auth import logout as auth_logout
from django.db.models import Q


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})

@login_required
def profile(request):
    profile = get_object_or_404(Profile, user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'profile.html', {'form': form, 'profile': profile})

@login_required
def dashboard(request):
    projects = request.user.projects.all()
    return render(request, 'dashboard.html', {'projects': projects})

@login_required
def project_detail(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    tasks = Task.objects.filter(project=project)


    status = request.GET.get('status')
    priority = request.GET.get('priority')
    due_date = request.GET.get('due_date')

    if status:
        tasks = tasks.filter(status=status)
    if priority:
        tasks = tasks.filter(priority=priority)
    if due_date:
        tasks = tasks.filter(due_date=due_date)

    return render(request, 'project_detail.html', {
        'project': project,
        'tasks': tasks,
    })

@login_required
def create_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save()
            project.members.add(request.user)
            return redirect('dashboard')
    else:
        form = ProjectForm()
    return render(request, 'create_project.html', {'form': form})

@login_required
def create_task(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.project = project
            task.save()
            return redirect('project_detail', pk=project_id)
    else:
        form = TaskForm()
    return render(request, 'task_form.html', {'form': form, 'project': project})

@login_required
def task_detail(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.task = task
            comment.user = request.user
            comment.save()
            return redirect('task_detail', task_id=task_id)
    else:
        comment_form = CommentForm()

    comments = task.comments.all()
    return render(request, 'task_detail.html', {
        'task': task,
        'comment_form': comment_form,
        'comments': comments
    })
def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'home.html')
@login_required
def profile_edit(request):
    profile = get_object_or_404(Profile, user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'profile_edit.html', {'form': form})
def logout(request):
    if request.user.is_authenticated:
        auth_logout(request)
    return redirect('login')
def edit_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_detail', pk=task.pk)
    else:
        form = TaskForm(instance=task)

    return render(request, 'edit_task.html', {'form': form, 'task': task})

def edit_project(request, pk):
    project = get_object_or_404(Project, pk=pk)

    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('project_detail', pk=project.pk)
    else:
        form = ProjectForm(instance=project)

    return render(request, 'edit_project.html', {'form': form, 'project': project})

@login_required
def project_chat(request, project_id):
    project = Project.objects.get(id=project_id)
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.project = project
            message.user = request.user
            message.save()
            return redirect('project_chat', project_id=project.id)
    else:
        form = MessageForm()
    messages = project.messages.all()
    context = {
        'project': project,
        'messages': messages,
        'form': form,
    }
    return render(request, 'project_chat.html', context)


def search(request):
    query = request.GET.get('query', '')
    projects = Project.objects.filter(name__icontains=query)
    users = User.objects.filter(username__icontains=query)
    return render(request, 'search_results.html', {
        'projects': projects,
        'users': users,
        'query': query,
    })

def user_detail(request, user_id):
    user = get_object_or_404(User, id=user_id)
    return render(request, 'user_detail.html', {'user': user})
