from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager

class PublishedManager(models.Manager):  # менеджера возвращает набор запросов QuerySet, который будет исполнен
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)  # Фильтрация постов по статусу "Опубликован"

class Post(models.Model):

    class Status(models.TextChoices):
        DRAFT = 'ЧН', 'Черновик'  # Статус "Черновик" для поста
        PUBLISHED = 'ОБ', 'Опубликован'  # Статус "Опубликован" для поста

    title = models.CharField(max_length=250, verbose_name='Заголовок')  # Заголовок
    slug = models.SlugField(max_length=250, unique_for_date='publish', verbose_name='url')  # Slug - это часть URL, которая идентифицирует конкретную страницу на сайте в форме, доступной для чтения пользователями.
    author = models.ForeignKey(User,  # Указывает автора поста.
                               on_delete=models.CASCADE,  # Связь многие к многим.
                               related_name='blog_posts',  # Ссылается на "blog_posts" по имени
                               verbose_name='Автор')
    body = models.TextField(verbose_name='Основной текст')  #Тело поста
    publish = models.DateTimeField(default=timezone.now, verbose_name='Дата публикаций')  # Метод timezone.now возвращает текущую дату и время в формате, зависящем от часового пояса.
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создание')  # При применении параметра auto_now_add дата будет сохраняться автоматически во время создания объекта
    updated = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')  # Он будет использоваться для хранения последней даты и времени обновления поста.
    status = models.CharField(max_length=2,
                              choices=Status.choices,  # Статус поста, отображение "Черновик" или "Опубликован".
                              default=Status.DRAFT,
                              verbose_name='Статус')  # Статус поста по дефолту "Черновик".
    object = models.Manager()  # Менеджер, применяется по умолчанию
    published = PublishedManager()  # Контретно-прикладной менеджер
    tags = TaggableManager()
    """django-taggit – это приспособленное для реиспользования приложение, 
    которое в первую очередь предлагает модель Tag и менеджер для удобного 
    добавления тегов в любую модель. Исходный код приложения доступен для 
    просмотра на странице"""

    class Meta:
        ordering = ['-publish']  # Обратный порядок постов
        indexes = [
            models.Index(fields=['-publish']),  # Индексация в БД
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):  # ссылка из list.html для валидного отображения.
        return reverse('blog:post_detail',
                       args=[self.publish.year,
                             self.publish.month,
                             self.publish.day,
                             self.slug])


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE,  # Связать каждый коммент с постом
                             related_name='comments')
    # Атрибут related_name позволяет назначать имя атрибуту, который используется для связи от ассоциированного объекта назад к нему
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)  # создает метку при создании строки в базе
    updated = models.DateTimeField(auto_now=True)  # обновляет метку каждый раз при изменении
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created']
        indexes = [models.Index(fields=['created']),
                   ]

    def __str__(self):
        return f'Комментарий от {self.name} на {self.post}'
