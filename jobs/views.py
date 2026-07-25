from django.shortcuts import render, redirect,get_object_or_404
from .forms import JobRoleForm
from .models import JobRole

def job_list(request):
    jobs = JobRole.objects.all().order_by("-id")
    return render(request, "jobs/job_list.html", {"jobs": jobs})


def add_job(request):
    if request.method == "POST":
        form = JobRoleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("job_list")
    else:
        form = JobRoleForm()

    return render(request, "jobs/add_job.html", {"form": form})
def edit_job(request, job_id):
    job = get_object_or_404(JobRole, id=job_id)

    if request.method == "POST":
        form = JobRoleForm(request.POST, instance=job)

        if form.is_valid():
            form.save()
            return redirect("job_list")

    else:
        form = JobRoleForm(instance=job)

    return render(request, "jobs/add_job.html", {"form": form})
def delete_job(request, job_id):
    job = get_object_or_404(JobRole, id=job_id)

    job.delete()

    return redirect("job_list")