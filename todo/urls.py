from django.urls import path
from todo import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login', views.login, name='login'),
    path('signup', views.signup, name='signup'),
    path('add', views.add, name='add'),
    path('logout', views.signout, name='signout'),
    path('delete/<int:id>', views.delete, name='delete'),
    path('change/<int:id>/<str:status>', views.change,),
]
