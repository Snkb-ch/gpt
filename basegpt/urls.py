from . import views
from django.urls import path

urlpatterns = [
    path('exam-text', views.exam_text, name='exam_text'),
    path('uniquetext', views.uniquetext, name='uniquetext'),
    path('uniquefile', views.uniquefile, name='uniquefile'),
    path('success', views.success, name='success'),
    path('notifications', views.notifications.as_view(), name='notifications'),
    path('history', views.history, name='history'),


    path('get_objects', views.get_objects, name='get_objects'),


    path('logout/', views.logoutUser, name='logout'),

    path('', views.home, name='home'),
    path('unique', views.unique, name='unique'),
    path('cloud', views.cloud, name='cloud'),

    path('contact/', views.contact, name='contact'),
    path('error/', views.error, name='error'),
    path('audio/', views.audio, name='audio'),

 path('login/', views.CustomLoginView.as_view(), name='login'),

path('register/', views.RegisterPage.as_view(), name='register'),
    path('success_api', views.success_api, name='success_api'),
    path('success_result', views.success_result, name='success_result'),
path('exam_text_get_idea', views.exam_text_get_idea, name='exam_text_get_idea'),
    path('check_idea/<int:id>/', views.check_idea, name='check_idea'),



]
