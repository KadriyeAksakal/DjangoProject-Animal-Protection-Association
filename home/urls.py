from django.urls import path

from . import views

urlpatterns = [
    # ex: /home/    yani herhangi bir parametre girilmez ise home dizinine gidilsin
    path('', views.index, name='index'),
    # ex: /polls/5/
   # path('<int:question_id>/', views.detail, name='detail'),

]