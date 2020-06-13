from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('update/', views.user_update, name="user_update"),
    path('password/', views.change_password, name="change_password"),
    path('applications/', views.applications, name="applications"),
    path('comments/', views.comments, name="comments"),
    path('deletecomment/<int:id>', views.deletecomment, name="deletecomment"),
    #path('addcontent/<int:id>', views.addcontent, name="addcontent"),
    path('contents/', views.contents, name="contents"),
    path('addcontent/', views.addcontent, name="addcontent"),
    path('deletecontent/<int:id>', views.deletecontent, name="deletecontent"),
    path('deleteapplication/<int:id>', views.deleteapplication, name="deleteapplication"),
    path('editcontent/<int:id>', views.editcontent, name="editcontent"),
]