

from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', views.logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('project/<int:project_id>/', views.project_detail, name='project_detail'),
    path('project/create/', views.create_project, name='create_project'),
    path('project/<int:project_id>/task/create/', views.create_task, name='create_task'),
    path('task/<int:task_id>/', views.task_detail, name='task_detail'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
    path('task/<int:pk>/edit/', views.edit_task, name='edit_task'),
    path('project/<int:pk>/edit/', views.edit_project, name='edit_project'),
    path('accounts/password_reset/', auth_views.PasswordResetView.as_view(
        template_name='password_reset_form.html',
        email_template_name='password_reset_email.txt',
        subject_template_name='password_reset_subject.txt'
    ), name='password_reset'),
    path('accounts/password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'),
         name='password_reset_done'),
    path('accounts/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        form_class=auth_views.SetPasswordForm,
        template_name='password_reset_confirm.html'
    ), name='password_reset_confirm'),
    path('accounts/reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),
         name='password_reset_complete'),
    path('project/<int:project_id>/chat/', views.project_chat, name='project_chat'),
    path('search/', views.search, name='search'),
    path('user/<int:user_id>/', views.user_detail, name='user_detail'),

]

