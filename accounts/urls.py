from django.urls import path, include
from accounts import views

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('signin/', views.signin_view, name='signin'),
    path('logout/', views.logout_view, name='logout'),
    path('linkedin/auth/', views.linkedin_auth, name='linkedin_auth'), 
    path('linkedin/callback/', views.linkedin_callback, name='linkedin_callback'),
    path('', views.home, name='home'), 
]
