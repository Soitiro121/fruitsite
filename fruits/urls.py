from django.urls import path

from . import views

app_name = "fruits"
urlpatterns = [
    path('', views.list_fruits, name='index'),
    path("search/", views.search_fruits, name="search"),
    path("create/", views.create_fruit, name="create"),
    path('<int:pk>/review/', views.create_review, name='review'),
    path('<int:pk>/', views.FruitDetailView.as_view(), name="detail"),
    path('lists/', views.ListListView.as_view(), name='lists'),
    path('lists/create', views.ListCreateView.as_view(), name='create-list'),
]
