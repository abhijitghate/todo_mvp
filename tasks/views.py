from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.csrf import csrf_exempt
from .models import Task
from .forms import TaskForm


def index(request):
    tasks = Task.objects.all().order_by("-created_at").order_by("updated_at")
    context = {"tasks": tasks, "form": TaskForm()}
    return render(request, "tasks.html", context)


def task_search(request):  # Simulate a delay for demonstration purposes
    query = request.GET.get("search", "")
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
    return render(request, "fragments/task_list.html", context)


def create_task(request):
    if request.method == "POST":
        task = TaskForm(request.POST)
        if task.is_valid():
            _t = task.save()

    # context = {"task": _t}

    # response = render(request, "fragments/single_task.html", context)

    tasks = Task.objects.all().order_by("-created_at").order_by("updated_at")
    response = render(request, "fragments/task_list.html", {"tasks": tasks})
    response["HX-Trigger"] = "success"
    return response


# @csrf_exempt
def delete_task(request, pk):
    if request.method == "DELETE":
        task = get_object_or_404(Task, pk=pk)
        task.delete()
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
        if request.method == "POST":
            form = TaskForm(request.POST, instance=task)
            if form.is_valid():
                _task = form.save()
                response = render(
                    request, "fragments/single_task.html", {"task": _task}
                )
                response["HX-Trigger"] = "task-updated"
                return response
        else:
            form = TaskForm(instance=task)
    except Exception as e:
        print("Error updating task:", e)
    return HttpResponse(status=500)


def bulk_delete_tasks(request):
    if request.method == "POST":
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
            return HttpResponse(str(e), status=400)
    return HttpResponse("Method not allowed", status=405)
