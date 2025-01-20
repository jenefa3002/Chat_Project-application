from django.urls import path
from .views import chat_view, signup
from . import views

urlpatterns = [
    path('', chat_view, name='chat'),
    path('signup/', signup, name='signup'),
    path('save_message/', views.save_message, name='save_message'),
]
