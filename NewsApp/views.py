from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import News, Category
from django.views.generic import ListView, TemplateView, UpdateView, DeleteView, CreateView
from .forms import ContactForm, CommentForm
from django.urls import reverse_lazy
from hitcount.views import HitCountDetailView, get_hitcount_model, HitCountMixin
from .custom_permissions import OnlyLoggedSuperUser


def news_list(request):
    # news_list = News.objects.filter(status=News.Status.Published)
    news_list = News.published.all()
    context = {
        "news_list": news_list,
    }
    return render(request, 'news/index.html', context)


def homePageView(request):
    news_list = News.published.all().order_by('-publish_time')[:4]
    local_news = News.published.all().filter(category__name='Mahalliy').order_by('-publish_time')[:4]
    foreign_news = News.published.all().filter(category__name='Xorij').order_by('-publish_time')[:4]
    sport_news = News.published.all().filter(category__name='Sport').order_by('-publish_time')[:4]
    technology_news = News.published.all().filter(category__name='Texnologiya').order_by('-publish_time')[:4]
    categories = Category.objects.all()
    context = {
        "news_list": news_list,
        'local_news': local_news,
        'foreign_news': foreign_news,
        'sport_news': sport_news,
        'technology_news': technology_news,
        'categories': categories,
    }
    return render(request, "news/home.html", context)


class LocalNewsView(ListView):
    model = News
    context_object_name = 'local_news'
    template_name = 'news/local_news.html'

    def get_queryset(self):
        news = self.model.published.all().filter(category__name="Mahalliy")
        return news


class ForeignNewsView(ListView):
    model = News
    context_object_name = 'foreign_news'
    template_name = 'news/foreign_news.html'

    def get_queryset(self):
        news = self.model.published.all().filter(category__name="Xorij")
        return news


class TechnologyNewsView(ListView):
    model = News
    context_object_name = 'technology_news'
    template_name = 'news/technology_news.html'

    def get_queryset(self):
        news = self.model.published.all().filter(category__name='Texnologiya')
        return news


class SportNewsView(ListView):
    model = News
    context_object_name = 'sport_news'
    template_name = 'news/sport_news.html'

    def get_queryset(self):
        news = self.model.published.all().filter(category__name='Sport')
        return news


def news_detail(request, slug):
    news = get_object_or_404(News, slug=slug, status=News.Status.Published)

    context = {}
    hit_count = get_hitcount_model().objects.get_for_object(news)
    hits = hit_count.hits
    hitcontext = context['hitcount'] = {'pk': hit_count.pk}
    hit_count_responce = HitCountMixin.hit_count(request, hit_count)
    if hit_count_responce.hit_counted:
        hits = hits + 1
        hitcontext['hit_counted'] = hit_count_responce.hit_counted
        hitcontext['hit_message'] = hit_count_responce.hit_message
        hitcontext['total_hits'] = hits

    comments = news.comments.filter(active=True)
    comment_count = comments.count()
    new_comment = None
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.news = news
            new_comment.user = request.user
            new_comment.save()
            comment_form = CommentForm()
    else:
        comment_form = CommentForm()
    context = {
        "news": news,
        "comments": comments,
        "new_comment": new_comment,
        "comment_form": comment_form,
        "comment_count": comment_count,
    }
    return render(request, 'news/news_detail.html', context)


class ContactPageView(TemplateView):
    template_name = 'news/contact.html'

    def get(self, request):
        form = ContactForm()
        context = {
            "form": form,
        }
        return render(request, 'news/contact.html', context)

    def post(self, request):
        form = ContactForm(request.POST)
        if request.method == 'POST' and form.is_valid():
            form.save()
            return HttpResponse("<h1> Biz bilan bog'langaniz uchun tashakkur ")
        context = {
            "form": form,
        }
        return render(request, 'news/contact.html', context)


class NewsUpdateView(OnlyLoggedSuperUser, UpdateView):
    model = News
    fields = ['title', 'body', 'image', 'category', 'status']
    template_name = 'crud/news_edit.html'


class NewsDeleteView(OnlyLoggedSuperUser, DeleteView):
    model = News
    template_name = 'crud/news_delete.html'
    success_url = reverse_lazy('home_page')


class NewsCreateView(OnlyLoggedSuperUser, CreateView):
    model = News
    template_name = 'crud/news_create.html'
    fields = ['title', 'title_uz', 'title_en', 'title_ru',
              'slug', 'body', 'body_uz', 'body_en', 'body_ru',
              'image', 'category', 'status', 'user']


class SearchResultList(ListView):
    model = News
    template_name = 'news/search_result.html'
    context_object_name = 'all_news'

    def get_queryset(self):
        search = self.request.GET.get('q')
        return News.objects.filter(
            Q(title__icontains=search) | Q(body__icontains=search)
        )
