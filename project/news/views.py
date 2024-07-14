from datetime import datetime

from django.http import HttpResponse
from django.views import View
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView, SearchView,
)
from django.contrib.auth.decorators import login_required
from django.db.models import Exists, OuterRef
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect

from .filters import NewsFilter
from .forms import NewsForm
from django.shortcuts import render
from .models import News, Subscription, Category
import logging

logger = logging.getLogger(__name__)

from .tasks import send_email_task, weekly_send_email_task
from django.utils.translation import gettext as _ # импортируем функцию для перевода
from django.utils import timezone
from django.shortcuts import redirect
import pytz #  импортируем стандартный модуль для работы с часовыми поясами


class NewsList(ListView):
    model = News
    ordering = '-dateCreation'
    template_name = 'news.html'
    context_object_name = 'id_новости'
    paginate_by = 3

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['current_time'] = timezone.localtime(timezone.now())
        context['timezones'] = pytz.common_timezones
        return context

    def post(self, request):
        request.session['django_timezone'] = request.POST['timezone']
        return redirect(self.request.path)

class NewsDetail(DetailView):
    model = News
    template_name = 'news.html'
    context_object_name = 'id_новости'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        return context

class NewsCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_news',)
    # raise_exception = True
    form_class = NewsForm
    model = News
    template_name = 'news_edit.html'
    context_object_name = 'create'
    # success_url = reverse_lazy('news')

    def form_valid(self, form):
        post = form.save(commit=False)
        if self.request.path == '/articles/create/':
            news.categoryType = 'AR'
        elif self.request.path == '/news/create/':
            news.categoryType = 'NW'
            news.save()
            send_email_task.delay(post.pk)
        return super().form_valid(form)

class NewsUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_news',)
    form_class = NewsForm
    model = News
    template_name = 'news_edit.html'
    context_object_name = 'news'
    success_url = reverse_lazy('news')

class NewsDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_news',)
    model = News
    template_name = 'news_delete.html'
    context_object_name = 'delete'
    success_url = reverse_lazy('news_list')

class NewsSearch(ListView):
    model = News
    ordering = '-dateCreation'
    template_name = 'news_search.html'
    context_object_name = 'id_новости'
    paginate_by = 3

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = NewsFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context

@login_required
@csrf_protect
def subscriptions(request):
    if request.method == 'POST':
        category_id = request.POST.get('category_id')
        category = Category.objects.get(id=category_id)
        action = request.POST.get('action')

        if action == 'subscribe':
            Subscription.objects.create(user=request.user, category=category)
        elif action == 'unsubscribe':
            Subscription.objects.filter(
                user=request.user,
                category=category,
            ).delete()

    categories_with_subscriptions = Category.objects.annotate(
        user_subscribed=Exists(
            Subscription.objects.filter(
                user=request.user,
                category=OuterRef('pk'),
            )
        )
    ).order_by('name')
    return render(
        request,
        'subscriptions.html',
        {'categories': categories_with_subscriptions},
    )

# Create your views here.

# class Index(View):
#     def get(self, request):
#         models = News.objects.all()
#         context = {
#             'models': models,
#             'current_time': timezone.localtime(timezone.now()),
#             'timezones': pytz.common_timezones
#         }
#         return HttpResponse(render(request, 'news.html', context))
#
#         #  по пост-запросу будем добавлять в сессию часовой пояс, который и будет обрабатываться написанным нами ранее middleware
#     def post(self, request):
#         request.session['django_timezone'] = request.POST['timezone']
#         return redirect('/')