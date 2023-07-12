from django.shortcuts import render, get_object_or_404
from .models import Post
from django.views.generic import ListView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger  # вроде как список страниц, а EmptyPage это \
# обработка ошибки когда вызываешь не сущ. страницу списка, PageNotAnInteger обработка ошибки не правильного url поста
from .forms import EmailPostForm
from django.core.mail import send_mail

def post_share(request, post_id):
    # Извлечь пост по id
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)  # извлечь опубликованный пост по его id
    sent = False

    if request.method == 'POST':
        # Форма была передана на обработку
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_url(post.get_absolute_url())
            subject = f"{cd['name']} рекомендует вам прочитать {post.title}"
            message = f"Прочитайте {post.title} в {post_url}\n\n" \
            f"от {cd['name']} комментарий: {cd['comments']}"
            send_mail(subject, message, "bolket45@yandex.ru", [cd['to']])
            sent = True
            #... отправить электронное письмо
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post,
                                                    'form': form,
                                                    'sent': sent})

def post_detail(request, year, month, day, post):  # Это представление детальной информации о посте.
    post = get_object_or_404(Post,  # Ошибка 404
                             status=Post.Status.PUBLISHED,
                             slug=post,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    return render(request,
                'blog/post/detail.html',
                {'post': post})

class PostListView(ListView):
    """Альтернативное предстваление списка постов"""
    queryset = Post.published.all()  # используется для того, чтобы иметь конкретно-прикладной набор запросов QuerySet, не извлекая все объекты
    context_object_name = 'posts'  # переменная posts используется для результатов запроса.
    # Если не указано имя контекстного объекта context_object_name, то по умолчанию используется переменная object_list;
    paginate_by = 5  # постраничная разбивка результатов
    template_name = 'blog/post/list.html'  # конкретно-прикладной шаблон используется для прорисовки страницы шаблоном template_name