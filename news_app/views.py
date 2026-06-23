from multiprocessing import context
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import News, Category
from django.views.generic import TemplateView, CreateView, ListView
from .forms import ContactForm, NewsForm, CommentForm
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from news_project.custom_permissions import OnlyLoggedSuperUser
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q
from hitcount.utils import get_hitcount_model
from hitcount.views import HitCountMixin
# Create your views here.
from .forms import NewsForm

# def add_news(request):
#     if request.method == 'POST':
#         form = NewsForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('news_detail')
#     else:
#         form = NewsForm()
    
#     return render(request, 'news/news_create.html', {'form': form})

def news_list(request):
    news_list = News.published.all()
    context = {
        "news_list": news_list
    }
    return render(request, "news/news_list.html", context)


# class PostCountHitDetailView(HitCountDetailView):
#     model = News        # your model goes here
#     count_hit = True    # set to True if you want it to try and count the hit

def news_detail(request, id):
    news = get_object_or_404(News, id=id, status = News.Status.Published)    
    news_list = News.published.all().order_by("-publish_time")[:10]
    categories = Category.objects.all()
    hit_count = get_hitcount_model().objects.get_for_object(news)
    hits = hit_count.hits
    hitcontext = {'pk': hit_count.pk}
    hit_count_response = HitCountMixin.hit_count(request, hit_count)
    if hit_count_response.hit_counted:
        hits = hits + 1
        hitcontext['hit_counted'] = hit_count_response.hit_counted
        hitcontext['hit_message'] = hit_count_response.hit_message
        hitcontext['total_hits'] = hits

    # news.view_count += 1
    # news.save()
    comments = news.comments.filter(active=True)
    comments_count = comments.count()
    new_comment = None
    if request.method == "POST":
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
        "comments_count": comments_count,
        'new_comment': new_comment,
        "comment_form": comment_form,
        "news_list": news_list,
        "categories": categories,
        "hitcontext": hitcontext,
    }
    return render(request, "news/news_detail.html", context)

# def HomePageView(request):
#     news_list = News.published.all().order_by("-publish_time")[:3]
#     categories = Category.objects.all()
#     context = {
#         "news_list": news_list,
#         "categories": categories
#     }
#     return render(request, "news/index.html", context)

class HomePageView(TemplateView):
    model = News
    template_name = "news/index.html"
    context_object_name = "news_list"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["slider_news"] = self.model.published.all().order_by("-publish_time")[:5]
        context["categories"] = Category.objects.all()
        context["news_list"] = self.model.published.all().order_by("-publish_time")
        return context

# def contactPageView(request):
#     form = ContactForm(request.POST or None)
#     if request.method == "POST" and form.is_valid():
#         form.save()
#         return HttpResponse("<h2> Thank you </h2>")
#     context = {
#         "form":form
#     }
#     return render(request, "news/contact.html", context)

class ContactPageView(TemplateView):
    template_name = "news/contact.html"
    
    def get(self, request, *args, **kwargs):
        form = ContactForm()
        context = {
            "form": form
        }
        return render(request, "news/contact.html", context)
    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST)
        if form.is_valid() and request.method == "POST":
            form.save()
            return HttpResponse("<h2> Thank you for connecting with us</h2>")
        context = {
            "form": form
        }
        return render(request, "news/contact.html", context)
def categoryPageView(request):
    context = {
        "categories": Category.objects.all(),
        "news_list": News.published.all().order_by("-publish_time")
    }
    return render(request, "news/category.html", context)

# def singlePageView(request, id):
#     context = {
#         "news": get_object_or_404(News, id=id),
#         "news_list": News.published.all().order_by("-publish_time")[:10],
#         "categories": Category.objects.all()
#     }
#     return render(request, "news/single.html", context)
def singlePageView(request):
    context = {
        "categories": Category.objects.all(),
        "news_list": News.published.all().order_by("-publish_time")[:10]
    }
    return render(request, "news/single.html", context)

# def news_create(request):
#     if request.method == 'POST':
#         form = NewsForm(request.POST, request.FILES) # request.FILES juda muhim!
#         if form.is_valid():
#             form.save()
#             return redirect('all_news_list')
#     else:
#         form = NewsForm()
#     return render(request, 'news/create.html', {'form': form})

class NewsCreateView(OnlyLoggedSuperUser, CreateView):
    model = News
    template_name = 'news/create.html'
    fields = ['title', 'title_en', 'title_ru', 'title_uz', 'slug', 'body', 'body_en', 'body_ru', 'body_uz', 'image', 'category', 'status']

@login_required
@user_passes_test(lambda u:u.is_superuser)
def admin_page_view(request):
    admin_users = User.objects.filter(is_superuser=True)
    context = {
        "admin_users": admin_users
    }
    return render(request, "pages/admin_page.html", context)

class SearchResultsView(ListView):
    model = News
    template_name = 'news/search_results.html'
    context_object_name = 'news_list'
    
    def get_queryset(self):
        query = self.request.GET.get('q')
        return News.objects.filter(
            Q(title__icontains=query) | Q(body__icontains=query)
        )
    