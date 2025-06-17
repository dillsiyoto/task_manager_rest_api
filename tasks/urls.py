from django.urls import path
from .views import CreateTaskView, MyTasksView

urlpatterns = [
    path("create_task/", CreateTaskView.as_view(), name="create_task"),
    path("my_tasks/", MyTasksView.as_view(), name="my_tasks"),
]