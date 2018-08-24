from django.http import HttpResponseRedirect
from django.views import generic
from .models import Project, AppForProject
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from fairapp.forms import SignUpForm
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from .filters import ProjectFilter
from .forms import UserForm, ProfileForm
from django.contrib.auth.decorators import login_required, permission_required
from django.db import transaction
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.contrib.auth.models import User


def index(request, page=1):
    object_list = Project.objects.all().exclude(status__in=['m', 'r'])
    project_filter = ProjectFilter(request.GET, queryset=object_list)
    project_list = project_filter.qs
    paginator = Paginator(project_list.order_by('-pub_date'), 5)
    if page > paginator.num_pages:
        page = 1
    try:
        projects = paginator.get_page(page)
    except EmptyPage:
        projects = paginator.page(paginator.num_pages)
    return render(request, 'fairapp/index.html', {'page': page,
                                                  'projects': projects,
                                                  'filter': project_filter,
                                                  })


@login_required
def view_profile_projects(request, page=1):
    project_list = Project.objects.all().filter(members__in=[request.user.id])
    paginator = Paginator(project_list.order_by('-pub_date'), 5)
    if page > paginator.num_pages:
        page = 1
    try:
        projects = paginator.get_page(page)
    except EmptyPage:
        projects = paginator.page(paginator.num_pages)
    return render(request, 'fairapp/myprojects.html', {'page': page,
                                                       'projects': projects,
                                                       })


@login_required
def view_profile_applications(request, page=1):
    object_list = AppForProject.objects.all().filter(user__in=[request.user])
    paginator = Paginator(object_list.order_by('-id'), 5)
    if page > paginator.num_pages:
        page = 1
    try:
        apps = paginator.get_page(page)
    except EmptyPage:
        apps = paginator.page(paginator.num_pages)
    return render(request, 'fairapp/myapplications.html', {'page': page,
                                                         'apps': apps,
                                                         })


@permission_required('fairapp.approve_project')
def moderator_index(request, page=1):
    object_list = Project.objects.all().filter(status='m')
    paginator = Paginator(object_list.order_by('-pub_date'), 5)
    if page > paginator.num_pages:
        page = 1
    try:
        projects = paginator.get_page(page)
    except EmptyPage:
        projects = paginator.page(paginator.num_pages)
    return render(request, 'fairapp/index.html', {'page': page,
                                                  'projects': projects,
                                                  })


@permission_required('fairapp.approve_application')
def moderator_applications(request, page=1):
    object_list = AppForProject.objects.all().filter(status='m')
    paginator = Paginator(object_list.order_by('-id'), 5)
    if page > paginator.num_pages:
        page = 1
    try:
        apps = paginator.get_page(page)
    except EmptyPage:
        apps = paginator.page(paginator.num_pages)
    return render(request, 'fairapp/applications.html', {'page': page,
                                                         'apps': apps,
                                                         })


class ModerDetailView(PermissionRequiredMixin, generic.DetailView):
    permission_required = 'fairapp.approve_project'
    model = Project
    template_name = 'fairapp/moderdetails.html'


class ModerAppDetailView(PermissionRequiredMixin, generic.DetailView):
    permission_required = 'fairapp.approve_application'
    model = AppForProject
    template_name = 'fairapp/moderappdetails.html'


class IndexView(generic.ListView):
    template_name = 'fairapp/index.html'
    context_object_name = 'latest_project_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Project.objects.order_by('pub_date')[:5]


class DetailView(generic.DetailView):
    model = Project
    template_name = 'fairapp/details.html'


class ProjectCreate(LoginRequiredMixin, CreateView):
    model = Project
    fields = ('project_name', 'pub_date', 'start_date', 'end_date', 'brief_summary', 'content',
              'app_deadline', 'num_places', 'type', 'tag', 'skill')

    def form_valid(self, form):
        form.save()
        form.instance.head.add(self.request.user)
        form.save()
        return super(ProjectCreate, self).form_valid(form)


class ProjectUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = 'fairapp.edit_project'
    model = Project
    fields = '__all__'


class ProjectDelete(PermissionRequiredMixin, DeleteView):
    permission_required = 'fairapp.delete_project'
    model = Project
    success_url = reverse_lazy('fairapp:index')


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('fairapp:index')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})


def search(request):
    project_list = Project.objects.all()
    project_filter = ProjectFilter(request.GET, queryset=project_list)
    return render(request, 'fairapp/search_projects.html', {'filter': project_filter})


@login_required
@transaction.atomic
def update_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('/profile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'fairapp/profile_update.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })


@login_required
def view_profile(request):
    profile = request.user.profile
    return render(request, 'fairapp/profile.html', {"profile": profile})


class ApplicationCreate(LoginRequiredMixin, CreateView):
    model = AppForProject
    fields = ('covering_letter', )

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.project = Project.objects.get(pk=self.kwargs['pk'])
        form.instance.status = 'm'
        form.save()
        return super(ApplicationCreate, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ApplicationCreate, self).get_context_data()
        context['pk'] = self.kwargs['pk']
        return context


@permission_required('fairapp.approve_project')
def approve_project(request, pk):
    obj = Project.objects.get(pk=pk)
    if request.POST['Decision'] == 'approve':
        obj.status = 'c'
    elif request.POST['Decision'] == 'reject':
        obj.status = 'r'
    obj.save()
    return redirect('fairapp:index')


@permission_required('fairapp.approve_application')
def approve_application(request, pk):
    obj = AppForProject.objects.get(pk=pk)
    if request.POST['Decision'] == 'approve':
        obj.project.members.add(obj.user)
        obj.status = 'a'
    elif request.POST['Decision'] == 'reject':
        obj.status = 'r'
    obj.save()
    return redirect('fairapp:index')


class ApplicationView(LoginRequiredMixin, generic.DetailView):
    model = AppForProject
    fields = '__all__'
