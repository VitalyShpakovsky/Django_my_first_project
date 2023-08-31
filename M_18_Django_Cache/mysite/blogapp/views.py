from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView
from .models import Article


class ArticleListView(ListView):
    """Вывод списка статей."""

    queryset = (
        Article.objects.defer("content", "id").select_related("author", "category").prefetch_related("tags")
    )


class ArticleCreateView(CreateView):
    """Создание новой статьи."""

    model = Article
    fields = "title", "content", "author", "category", "tags"
    success_url = reverse_lazy("blogapp:article_list")
