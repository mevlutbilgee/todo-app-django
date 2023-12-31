from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

# Imports for Reordering Feature
from django.views import View
from django.db import transaction

from .models import Task
from .forms import PositionForm

import django_filters
from django_filters import ChoiceFilter
from django.shortcuts import render
from django.db.models import Q

class TaskFilter(django_filters.FilterSet):
    category = django_filters.ChoiceFilter(field_name='category', choices=Task.CATEGORY_CHOICES)
    search = django_filters.CharFilter(field_names=['title', 'description'])
    class Meta:
        model = Task
        fields = ['category', 'search']



def task_list(request):
    tasks = Task.objects.all()

    # Django filter kütüphanesini kullanarak filtreleme işlemini gerçekleştirin.
    task_filter = TaskFilter(request.GET, queryset=Task.objects.all())
    tasks = task_filter.qs

    return render(request, 'task_list.html', {
        'tasks': tasks
    })

class CustomLoginView(LoginView):
    template_name = 'base/index.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('tasks')


class RegisterPage(FormView):
    template_name = 'base/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(RegisterPage, self).get(*args, **kwargs)



class TaskList(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        context['count'] = context['tasks'].filter(complete=False).count()
        search_input = self.request.GET.get('search') or ''
        category_filter = self.request.GET.get('category')  # Seçilen kategori
        if search_input:
            context['tasks'] = context['tasks'].filter(
                title__contains=search_input) | context['tasks'].filter(description__contains=search_input)
        if category_filter:  # Kategoriye göre filtreleme
            context['tasks'] = context['tasks'].filter(category=category_filter)
        context['search_input'] = search_input
        context['selected_category'] = category_filter  # Şu an seçili olan kategori
        return context


class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'base/task.html'


class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['title', 'description', 'complete', 'category']
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)


class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['title', 'description', 'complete', 'category']
    success_url = reverse_lazy('tasks')
    def get_queryset(self):
        owner = self.request.user
        return self.model.objects.filter(user=owner,is_deleted=False)


class DeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('tasks')
    def get_queryset(self):
        owner = self.request.user
        return self.model.objects.filter(user=owner,is_deleted=False)

class TaskReorder(View):
    def post(self, request):
        form = PositionForm(request.POST)

        if form.is_valid():
            positionList = form.cleaned_data["position"].split(',')

            with transaction.atomic():
                self.request.user.set_task_order(positionList)

        return redirect(reverse_lazy('tasks'))

