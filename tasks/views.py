from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from .serializers import TaskSerializer
from .models import Task

class CreateTaskView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            task = serializer.save(owner = request.user)
            return Response(
                data={"message": "task succesfully created"},
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )


class MyTasksView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        tasks = Task.objects.filter(owner = request.user)

        status_param = request.query_params.get("status")
        if status_param:
            tasks = tasks.filter(status = status_param)

        ordering = request.query_params.get("ordering")
        if ordering == "asc":
            tasks = tasks.order_by("due_date")
        elif ordering == "desc":
            tasks = tasks.order_by("-due_date")

        serializer = TaskSerializer(tasks, many = True)
        return Response(serializer.data)
    

class TaskDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_task(self, pk, user):
        return get_object_or_404(Task, pk=pk, owner=user)
    
    def get(self, request, pk):
        task = self.get_task(pk, request.user)
        serializer = TaskSerializer(task)
        return Response(serializer.data)
    
    def put(self, request, pk):
        task = self.get_task(pk, request.user)
        serializer = TaskSerializer(task, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        task = self.get_task(pk, request.user)
        task.delete()
        return Response({"message": "task deleted"}, status=status.HTTP_204_NO_CONTENT)