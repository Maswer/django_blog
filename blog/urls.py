from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.PostListView.as_view(), name='post_list'),  # добавив новый шаблон URL адреса, используя класс PostListView
    path('<int:year>/<int:month>/<int:day>/<slug:post>/',  # Выводит url с годом/месяцем/день/слаг.
         views.post_detail,
         name='post_detail'),# Детали поста
    path('<int:post_id>/share/', views.post_share, name='post_share'),
]