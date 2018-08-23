from . import views
from django.urls import include, path

app_name = 'fairapp'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:page>/', views.index, name='index'),
    path('projects/<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('projects/create/', views.ProjectCreate.as_view(), name='project_create'),
    path('projects/<int:pk>/sendapp/', views.ApplicationCreate.as_view(), name='application_create'),
    path('projects/<int:pk>/approve/', views.approve_project, name='approveproject'),
    path('projects/<int:pk>/update/', views.ProjectUpdate.as_view(), name='project_update'),
    path('projects/<int:pk>/delete/', views.ProjectDelete.as_view(), name='project_delete'),
    path('signup/', views.signup, name='signup'),
    path('projects/search/', views.search, name='search'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('profile/', views.view_profile, name='view_profile'),
    path('profile/update/', views.update_profile, name='update_profile'),
    path('moderation/applications/apps/<int:pk>/approve/', views.approve_application, name='approveapp'),
    path('moderation/', views.moderator_index, name='moderindex'),
    path('moderation/<int:page>/', views.moderator_index, name='moderindex'),
    path('moderation/projects/<int:pk>/', views.ModerDetailView.as_view(), name='moderdetail'),
    path('moderation/applications/', views.moderator_applications, name='moderapplications'),
    path('moderation/applications/<int:page>/', views.moderator_applications, name='moderapplications'),
    path('moderation/applications/apps/<int:pk>/', views.ModerAppDetailView.as_view(), name='moderdetailapplication'),
]
