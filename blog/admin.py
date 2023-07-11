from django.contrib import admin
from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'author', 'publish', 'status']  # Список полей отображаемые в админке.
    list_filter = ['status', 'created', 'publish', 'author']  # Список содержит правую боковую панель, которая позволяет фильтровать результаты по полям
    search_fields = ['title', 'body']  # Строка поиска по полям, по которым можно выполнять поиск.
    prepopulated_fields = {'slug': ('title',)}  # предзаполнять поле slug данными, вводимыми в поле title.
    raw_id_fields = ['author']  # отображается поисковым виджетом, который будет более приемлемым, чем выбор из выпадающего списка, когда у вас тысячи пользователей
    date_hierarchy = 'publish'  # навигационные ссылки для навигации по иерархии дат.
    ordering = ['status', 'publish']  # По умолчанию посты упорядочены по столбцам STATUS и PUBLISH.