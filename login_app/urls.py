from django.urls import path     
from . import views
urlpatterns = [
    path('', views.index),	  
    path('login', views.login), 
    path('register', views.register), 
    path('logout', views.logout), 
    path('<str:firstname>/account', views.my_trees),
    path('delete/<int:tree_id>', views.delete_tree),
    path('new/tree', views.show_add_tree),
    path('new/add_tree', views.add_tree),
    path('show/<int:tree_id>', views.tree_details),
    path('edit/<int:tree_id>', views.edit_tree),
    path('edit/update_tree/<int:tree_id>', views.update_tree),





]

