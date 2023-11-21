from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.shortcuts import render, get_object_or_404
from .temp_data import fruit_data
from .models import Fruit, Review, List
from django.views import generic
from .forms import ReviewForm
from django.contrib.auth.decorators import login_required, permission_required


class FruitDetailView(generic.DetailView):
    model = Fruit
    template_name = 'fruits/detail.html'


class ListListView(generic.ListView):
    model = List
    template_name = 'fruits/lists.html'


class ListCreateView(generic.CreateView):
    model = List
    template_name = 'fruits/create_list.html'
    fields = ['name', 'author', 'fruits']
    success_url = reverse_lazy('fruits:lists')


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


@login_required
@permission_required('fruits.add_fruit')
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

@login_required
def create_review(request, fruit_id):
    fruit = get_object_or_404(Fruit, pk=fruit_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review_author = request.user
            review_text = form.cleaned_data['text']
            fruit.review_set.create(author=review_author, text=review_text)
            return HttpResponseRedirect(
                reverse('fruits:detail', args=(pk, )))
    else:
        form = ReviewForm()
    context = {'form': form, 'fruit': fruit}
    return render(request, 'fruits/review.html', context)

def detail_fruit(request, fruit_id):
    fruit = get_object_or_404(Fruit, pk=fruit_id)
    request.session['last_viewed'] = fruit_id
    context = {'fruit': fruit}
    return render(request, 'fruits/detail.html', context)


def list_fruits(request):
    fruit_list = Fruit.objects.all()
    context = {'fruit_list': fruit_list}
    last_fruit_id = request.session.get('last_viewed', None)
    if last_fruit_id:
        context["last_fruit"] = Fruit.objects.get(pk=last_fruit_id)
    return render(request, 'fruits/index.html', context)