from . import views
from django.urls import path

urlpatterns = [

    path('adtext', views.uniquetext, name='uniquetext'),
    path('uniquefile', views.uniquefile, name='uniquefile'),
    path('success', views.success, name='success'),
    path('notifications', views.notifications.as_view(), name='notifications'),
    path('history', views.history, name='history'),


    path('get_objects', views.get_objects, name='get_objects'),


    path('logout/', views.logoutUser, name='logout'),
    path('get_balance', views.get_balance.as_view(), name='get_balance'),

    path('', views.home, name='home'),
    path('unique', views.unique, name='unique'),
    path('balance', views.balance, name='balance'),



    path('contact/', views.contact, name='contact'),
    path('error/', views.error, name='error'),


 path('login/', views.CustomLoginView.as_view(), name='login'),

path('register/', views.RegisterPage.as_view(), name='register'),
    path('success_api', views.success_api, name='success_api'),
    path('infotext', views.infotext.as_view(), name='infotext'),
    path('photo_api', views.photo_api.as_view(), name='photo_api'),

    path('photo', views.photo, name='photo'),
    path('infotext_result', views.infotext_result.as_view(), name='infotext_result'),
    path('success_result', views.success_result, name='success_result'),


    path('session/', views.session, name='session'),
    path('favorite', views.Favorite.as_view(), name='favorite'),
    path('user_rating', views.UserRating.as_view(), name='user_rating'),
    # path('chat/', views.chat_view, name='chat'),
    # path('chat-gpt', views.ChatGPTView.as_view(), name='chat_gpt'),
]