from django.urls import path
from .views import RegisterView, LoginView, ProfileView ,LogoutView ,ChatBotAPIView


urlpatterns = [
    
    path('', RegisterView.as_view()),
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('profile/', ProfileView.as_view()),
    path('logout/',LogoutView.as_view()) ,
    path('chatbot/',ChatBotAPIView.as_view()) 
    
]
