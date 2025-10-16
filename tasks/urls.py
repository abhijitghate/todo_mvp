from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("search/", views.task_search, name="search"),
    path("create/", views.create_task, name="create-task"),
    path("delete/<int:pk>/", views.delete_task, name="delete-task"),
    path("update/<int:pk>/", views.update_task, name="update-task"),
    path("bulk-delete/", views.bulk_delete_tasks, name="bulk-delete-tasks"),
]
