from django.shortcuts import render, get_object_or_404
from .models import Post
from django.views.generic import ListView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger  # вроде как список страниц, а EmptyPage это \
# обработка ошибки когда вызываешь не сущ. страницу списка, PageNotAnInteger обработка ошибки не правильного url поста
from .forms import EmailPostForm

def post_share(request, post_id):
    # Извлечь пост по id
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    if request.method == 'POST':
        # Форма была передана на обработку
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            #... отправить электронное письмо
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post,
                                                    'form': form})

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

def post_list(request):
    post_list = Post.published.all()
    # Постраничная разбивка с 5 постами на странице
    paginator = Paginator(post_list, 5)
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        # Если page_number не целое число, то
        # выдать первую страницу
        posts = paginator.page(1)
    except EmptyPage:
        # Если page_number находится вне диапазона, то
        # выдать последнюю страницу
        posts = paginator.page(paginator.num_pages)
    return render(request,
                  'blog/post/list.html',
                  {'posts': posts})

class PostListView(ListView):
    """Альтернативное предстваление списка постов"""
    queryset = Post.published.all()  # используется для того, чтобы иметь конкретно-прикладной набор запросов QuerySet, не извлекая все объекты
    context_object_name = 'posts'  # переменная posts используется для результатов запроса.
    # Если не указано имя контекстного объекта context_object_name, то по умолчанию используется переменная object_list;
    paginate_by = 5  # постраничная разбивка результатов
    template_name = 'blog/post/list.html'  # конкретно-прикладной шаблон используется для прорисовки страницы шаблоном template_name