from django.urls import path
from .views import RegisterView, LoginView, UserProfileView, CreateTodoView, UserTodoListView, UpdateTodoView, PartialUpdateTodoView, DeleteTodoView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('users/<int:user_id>/todos/create/', CreateTodoView.as_view(), name='create_todo'),
    path('users/<int:user_id>/todos/', UserTodoListView.as_view(), name='user_todos'),
    path('users/<int:user_id>/todos/<int:pk>/update/', UpdateTodoView.as_view(), name='update_todo'),
    path('users/<int:user_id>/todos/<int:pk>/partial-update/', PartialUpdateTodoView.as_view(), name='partial_update_todo'),
    path('users/<int:user_id>/todos/<int:todo_id>/delete/', DeleteTodoView.as_view(), name='delete_todo'),
]
