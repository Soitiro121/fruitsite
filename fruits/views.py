from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from .temp_data import fruit_data
from .models import Fruit
from django.views import generic
from .forms import FruitForm


class FruitListView(generic.ListView):
    model = Fruit
    template_name = 'fruits/index.html'


class FruitDetailView(generic.DetailView):
    model = Fruit
    template_name = 'fruits/detail.html'


def search_fruits(request):
    context = {}
    if request.GET.get("query", False):
        context = {
            "fruit_list": [
                m
                for m in fruit_data
                if request.GET["query"].lower() in m["name"].lower()
            ]
        }
    return render(request, "fruits/search.html", context)


def create_fruit(request):
    if request.method == 'POST':
        form = FruitForm(request.POST)
        if form.is_valid():
            fruit_name = form.cleaned_data['name']
            fruit_release_year = form.cleaned_data['release_year']
            fruit_poster_url = form.cleaned_data['poster_url']
            fruit = Fruit(name=fruit_name,
                          release_year=fruit_release_year,
                          poster_url=fruit_poster_url)
            fruit.save()
            return HttpResponseRedirect(
                reverse('fruits:detail', args=(fruit.id, )))
    else:
        form = FruitForm()
    context = {'form': form}
    return render(request, 'fruits/create.html', context)