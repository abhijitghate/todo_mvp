import logging
from django.http import HttpResponse, QueryDict
from django.shortcuts import get_object_or_404, render

from tasks.forms import TaskForm
from .models import Task
logger = logging.getLogger(__name__) 


def index(request):
    logger.info("Rendering index view")
    tasks = Task.objects.all().order_by("-created_at").order_by("updated_at")
    context = {"tasks": tasks, "form": TaskForm()}
    return render(request, "tasks.html", context)


def task_search(request):
    query = request.GET.get("search", "")
    logger.info(f"Task search initiated with query: {query}")
    if "completed" in request.GET:
        query = request.GET.get("completed")
        query = True if query.lower() == "true" else False
        tasks = (
            Task.objects.filter(completed=query)
            .order_by("-created_at")
            .order_by("updated_at")
        )
    else:
        tasks = (
            Task.objects.filter(title__icontains=query)
            .order_by("-created_at")
            .order_by("updated_at")
            if query
            else Task.objects.all().order_by("-created_at").order_by("updated_at")
        )
    context = {"tasks": tasks, "query": query}
    logger.info(f"{tasks.count()} tasks found for query '{query}'")
    return render(request, "fragments/task_list.html", context)


def create_task(request):
    if request.method == "POST":
        task = TaskForm(request.POST)
        if task.is_valid():
            _t = task.save()
            logger.info(f"Task created: {_t}")
        else:
            logger.error(f"Invalid task form submission: {task.errors}")

    tasks = Task.objects.all().order_by("-created_at").order_by("updated_at")
    response = render(request, "fragments/task_list.html", {"tasks": tasks})
    response["HX-Trigger"] = "success"
    return response


def delete_task(request, pk):
    if request.method == "DELETE":
        logger.info(f"Delete task request for pk={pk}")
        task = get_object_or_404(Task, pk=pk)
        task.delete()
        logger.info(f"Task deleted: pk={pk}")
        response = HttpResponse(status=204)
        response["HX-Trigger"] = "task-deleted"

        remaining_tasks = (
            Task.objects.all().order_by("-created_at").order_by("updated_at")
        )
        context = {"tasks": remaining_tasks}
        response = render(request, "fragments/task_list.html", context)
        return response
    else:
        return HttpResponse(status=405)


def update_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    try:
        if request.method == "PATCH":
            logger.info(f"Update task request for pk={pk}")
            data = QueryDict(request.body)
            form = TaskForm(data, instance=task)
            if form.is_valid():
                _task = form.save()
                response = render(
                    request, "fragments/single_task.html", {"task": _task}
                )
                response["HX-Trigger"] = "task-updated"
                return response
            else:
                return HttpResponse("Invalid data", status=400)
        else:
            return HttpResponse("Method Not Allowed", status=405)
    except Exception as e:
        logger.error(f"Error updating task: {e}")
        return HttpResponse(status=500)


def bulk_delete_tasks(request):
    if request.method == "DELETE":
        try:
            tasks = Task.objects.filter(completed=True)
            _, _ = tasks.delete()
            remaining_tasks = (
                Task.objects.all().order_by("-created_at").order_by("updated_at")
            )
            context = {"tasks": remaining_tasks}
            response = render(request, "fragments/task_list.html", context)
            response["HX-Trigger"] = "tasks-bulk-deleted"
            return response
        except Exception as e:
            logger.error(f"Error bulk deleting tasks: {e}")
            return HttpResponse(str(e), status=400)
    logger.error("Method not allowed for bulk deleting tasks")
    return HttpResponse("Method not allowed for bulk deleting tasks", status=405)
