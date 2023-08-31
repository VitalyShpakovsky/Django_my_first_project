from django.db import models


class Author(models.Model):
    """
    Модель **Author** представляет автора статьи,
    который имеет поля: имя 'name' и биография 'bio'.
    """

    class Meta:
        ordering = ["name"]

    name = models.CharField(max_length=100, db_index=True)
    bio = models.TextField(null=False, blank=True)

    def __str__(self) -> str:
        return f"Author(pk={self.pk}, name={self.name!r})"


class Category(models.Model):
    """
    Модель **Category** представляет категорию статьи,
    который имеет поле: название категории 'name'.
    """

    class Meta:
        ordering = ["name"]

    name = models.CharField(max_length=40, db_index=True)

    def __str__(self) -> str:
        return f"Category(pk={self.pk}, name={self.name!r})"


class Tag(models.Model):
    """
    Модель **Tag** представляет тэг статьи,
    который можно назначить статьи и имеет поле: название тэга 'name'.
    """

    class Meta:
        ordering = ["name"]

    name = models.CharField(max_length=20, db_index=True)

    def __str__(self) -> str:
        return f"Tag(pk={self.pk}, name={self.name!r})"


class Article(models.Model):
    """
    Модель **Article** представляет статью,
    которая имеет поля:
        tittle - заголовок статьи
        content - содержимое статьи
        pub_date - дата публикации статьи
        author - автор статьи
        category - категория статьи
        tags - тэги статьи
    """

    class Meta:
        ordering = ['author', 'title']

    title = models.CharField(max_length=200, db_index=True)
    content = models.TextField(null=False, blank=True)
    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)
