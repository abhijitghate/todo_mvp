from django.urls import path

from todo_app import settings
from . import views
from  django.conf.urls.static import static


urlpatterns = [
    path("", views.index, name="index"),
    path("search/", views.task_search, name="search"),
    path("create/", views.create_task, name="create-task"),
    path("delete/<int:pk>/", views.delete_task, name="delete-task"),
    path("update/<int:pk>/", views.update_task, name="update-task"),
    path("bulk-delete/", views.bulk_delete_tasks, name="bulk-delete-tasks"),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_URL)