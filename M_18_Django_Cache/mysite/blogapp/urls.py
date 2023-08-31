from django.urls import path

from .views import ArticleListView, ArticleCreateView


app_name = 'blogapp'


urlpatterns = [
    path("article/", ArticleListView.as_view(), name="article_list"),
    path("article/create/", ArticleCreateView.as_view(), name="create_article"),
    ]
