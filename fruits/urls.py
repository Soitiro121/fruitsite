from django.urls import path

from . import views

app_name = "fruits"
urlpatterns = [
    path("", views.FruitListView.as_view(), name="index"),
    path("search/", views.search_fruits, name="search"),
    path("create/", views.create_fruit, name="create"),
    path('<int:pk>/', views.FruitDetailView.as_view(), name='detail'),
]
