from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import RegisterSerializer, LoginSerializer, UserSerializer
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import TodoSerializer
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from .models import Todo
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.exceptions import ValidationError
from rest_framework.generics import UpdateAPIView
from django.shortcuts import get_object_or_404
from django.http import Http404 
from rest_framework.generics import DestroyAPIView

def get_object(self):
    """Fetch the specific todo object based on URL parameters."""
    todo_id = self.kwargs.get("todo_id")  # Get `todo_id` from URL
    user_id = self.kwargs.get("user_id")  # Get `user_id` from URL

    try:
        return Todo.objects.get(id=todo_id, user_id=user_id)
    except Todo.DoesNotExist:
        raise Http404({
            "status": 0,
            "message": "No Todo matches the given query.",
            "data": None
        })  # Return a response matching your structure


from rest_framework.permissions import BasePermission

class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


User = get_user_model()

class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': 1,
                'message': 'User registered successfully',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response({
            'status': 0,
            'message': 'Validation errors',
            'data': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)

        return Response({
            'status': 0,
            'message': 'Login failed',
            'data': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class UserProfileView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response({
            "status": 1,
            "message": "User profile fetched successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

class TodoPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 50

class CreateTodoView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = TodoSerializer(data=request.data, context={"request": request})

        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({
                "status": 1,
                "message": "Todo created successfully",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)

        # Handling validation errors inside our response format
        return Response({
            "status": 0,
            "message": "Validation error",
            "data": serializer.errors  # Returning validation errors properly
        }, status=status.HTTP_400_BAD_REQUEST)

# Get All Todos for a User (with pagination & search)
class UserTodoListView(ListAPIView):
    serializer_class = TodoSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = TodoPagination

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        search_query = self.request.query_params.get('search', '')

        return Todo.objects.filter(
            user_id=user_id
        ).filter(
            Q(title__icontains=search_query)
        ).order_by('-created_at')

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return Response({
            "status": 1,
            "message": "Todos fetched successfully",
            "data": response.data
        })

class UpdateTodoView(UpdateAPIView):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsOwner]
    lookup_field = 'pk'  # Explicitly define the lookup field

    def update(self, request, *args, **kwargs):
        todo = self.get_object()

        if todo.user != request.user:
            return Response({
                "status": 0,
                "message": "You can only update your own todos.",
                "data": None
            }, status=status.HTTP_403_FORBIDDEN)

        response = super().update(request, *args, **kwargs)
        return Response({
            "status": 1,
            "message": "Todo updated successfully",
            "data": response.data
        })

class PartialUpdateTodoView(UpdateAPIView):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsOwner]
    lookup_field = "pk"  

    def get_object(self):
        """Fetch the specific todo object based on URL parameters."""
        todo_id = self.kwargs.get("todo_id") 
        user_id = self.kwargs.get("user_id")  

        # Ensure the todo exists for the given user
        return get_object_or_404(Todo, id=todo_id, user_id=user_id)

    def patch(self, request, *args, **kwargs):
        """Handle PATCH requests with ownership validation."""
        todo = self.get_object()

        if todo.user != request.user:
            return Response({
                "status": 0,
                "message": "You can only update your own todos.",
                "data": None
            }, status=status.HTTP_403_FORBIDDEN)

        response = super().partial_update(request, *args, **kwargs)
        return Response({
            "status": 1,
            "message": "Todo updated successfully",
            "data": response.data
        }, status=status.HTTP_200_OK)

class DeleteTodoView(DestroyAPIView):
    """Delete a todo only if it belongs to the authenticated user."""
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsOwner]

    def get_object(self):
        """Fetch the specific todo object based on user_id and todo_id."""
        todo_id = self.kwargs.get("todo_id")  
        user_id = self.kwargs.get("user_id")  

        try:
            todo = Todo.objects.get(id=todo_id, user_id=user_id)
        except Todo.DoesNotExist:
            raise Http404({
                "status": 0,
                "message": "No Todo matches the given query.",
                "data": None
            })  

        if todo.user != self.request.user:
            return Response({
                "status": 0,
                "message": "You can only delete your own todos.",
                "data": None
            }, status=status.HTTP_403_FORBIDDEN)

        return todo

    def delete(self, request, *args, **kwargs):
        """Delete the task if it belongs to the user."""
        todo = self.get_object()
        todo.delete()
        return Response({
            "status": 1,
            "message": "Todo deleted successfully",
            "data": None
        }, status=status.HTTP_200_OK)