import os

# Create your views here.
import pandas as pd
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import Http404, get_object_or_404, redirect, render

from .forms import CompetitionForm
from .models import Competition, Rank
from django.contrib import messages


def create_competition(request):
    form = CompetitionForm(request.POST or None, request.FILES)

    if request.method == "POST" and request.POST and request.FILES:
        if form.is_valid():
            form.instance.user = request.user
            instance = form.save()
            return redirect("competition:detail", pk=instance.pk)

    return render(request, "competition/form.html",
                  {"form": form,
                   "button_name": "Create"})


def update_competition(request, pk):
    comp = get_object_or_404(Competition, pk=pk)
    form = CompetitionForm(instance=comp)

    if request.method == "POST":
        form = CompetitionForm(
            request.POST, files=request.FILES, instance=comp)

        if form.is_valid():
            form.instance.user = request.user
            form.save()
            return redirect("competition:detail", pk=pk)

    return render(request, "competition/form.html",
                  {"form": form,
                   "button_name": "Update"})


def view_competition_list(request):
    competitions = Competition.objects.all()
    return render(request, "competition/list.html", {"objects": competitions})


@login_required
def view_competition_detail(request, pk):
    obj = get_object_or_404(Competition, pk=pk)

    if request.method == "POST" and request.POST and request.FILES:
        csv_file = pd.read_csv(request.FILES["csv_file"])
        target_file = pd.read_csv(obj.test_answer_file)

        if csv_file.shape == target_file.shape:
            pred = csv_file.iloc[:, -1]
            target = target_file.iloc[:, -1]

            accuracy = (pred == target).mean()

            rank = Rank.objects.create(
                user=request.user, competition=obj, score=accuracy)
            rank.save()

        else:
            messages.add_message(request, messages.ERROR, "Wrong file shape")

    return render(request, "competition/detail.html", {"obj": obj})


def download(request, filepath):
    file_path = os.path.join(settings.MEDIA_ROOT, filepath)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(
                fh.read(), content_type="application/vnd.ms-excel")
            response[
                'Content-Disposition'] = 'inline; filename=' + os.path.basename(
                    file_path)
            return response
    raise Http404
