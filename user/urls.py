from django.urls import path

from . import views

urlpatterns = [
    # ex: /product/
    path('', views.index, name='index'),
    path('update/', views.user_update, name='user_update'),
    path('password/', views.change_password, name='change_password'),
    path('comments/', views.comments, name='comments'),
    path('deletecomment/', views.deletecomment, name='deletecomment'),
    path('addcontent/', views.addcontent, name='addcontent'),
    path('contents/', views.contents, name='contents'),    #listelemek için
    path('contentedit/', views.contentedit, name='contentedit'),
    path('contentdelete/', views.contentdelete, name='contentdelete'),

    # ex: /polls/5/
   # path('<int:question_id>/', views.detail, name='detail'),

]