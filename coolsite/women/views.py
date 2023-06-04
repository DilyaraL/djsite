from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.forms import model_to_dict
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.response import Response

from .forms import *
from .models import *
from .serializers import WomenSerializer
from .utils import *



class WomenHome(DataMixin, ListView):
    model = Women
    template_name = 'women/index.html'#по умолчанию будет искаться в имя приложения/имя модели_list.html
    context_object_name = 'posts'# по умолчанию называется object_list
    #extra_context = {'title': 'Главная страница'} #можно передавть только статические(неизмен) контекст


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)#что не затереть уже созданный уже контекст
        c_def = self.get_user_context(title='Главная страница')
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):#будем публиковать только с тру
        return Women.objects.filter(is_published=True).select_related('cat')
    #select_related - теперь будет реализован жадный запрос, теперь совмество с записями о женщинах is_published=True
    #будут загружены данные из таблицы Категории (cat-внешний ключ)

#def index(request):
#    posts = Women.objects.all()
#    context ={
#        'posts': posts,
#        'menu': menu,
#        'title': 'Главная страница',
#        'cat_selected': 0
#    }
#    return render(request, 'women/index.html', context=context)

@login_required
def about(request):
    return render(request, 'women/about.html', {'menu': menu, 'title': 'О сайте'})


class AddPage(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'women/addpage.html'
    success_url = reverse_lazy('home')# сюда перенаправимся после создания статьи, но тк у модели мы прописали get_absolute_url
    #то джанго нас на саму статьи и перенаправит
    login_url = reverse_lazy('home')
    raise_exception = True # чтобы вызывать ошибку 403

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)  # что не затереть уже созданный уже контекст
        c_def = self.get_user_context(title='Добавление статьи')
        return dict(list(context.items()) + list(c_def.items()))


# def addpage(request):
#     #если пользовтаель неправильно или нет заполнит форму, сервер вернет ее заполненой, а не пустой
#     if request.method =='POST':
#         form = AddPostForm(request.POST, request.FILES)
#         if form.is_valid():
#             #print(form.cleaned_data)
#             #можно не помещать в блок try except, тк он автоматичсеки так проверяет
#             form.save()
#             return redirect('home')
#     else:
#         form = AddPostForm()
#
#     return render(request, 'women/addpage.html', {'form': form, 'menu': menu, 'title': 'Добавление статьи'})


# def contact(request):
#     return HttpResponse(f"Обратная связь")

class ContactFormView(DataMixin, FormView):
    form_class = ContactForm
    template_name = 'women/contact.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)  # что не затереть уже созданный уже контекст
        c_def = self.get_user_context(title='Обратная связь')
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):# вызывается в случае если правильно заполнил форму
        print(form.cleaned_data)# выводим в терминале чистые данные, которые получили в форме
        return redirect('home')


# def login(request):
#     return HttpResponse(f"Авторизация")


class ShowPost(DataMixin,DetailView):
    model = Women
    template_name = 'women/post.html'#по умолчанию будет искаться в имя приложения/имя модели_list.html
    slug_url_kwarg = 'post_slug' # чтоб мы обращались именно по такому слагу а не просто slug
    #pk_url_kwarg = для id
    context_object_name = 'post'# в эту переменную будут помещенны данные из модели

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)  # что не затереть уже созданный уже контекст
        c_def = self.get_user_context(title=context['post'])
        return dict(list(context.items()) + list(c_def.items()))



# def show_post(request, post_slug):
#     post = get_object_or_404(Women, slug=post_slug)
#
#     context = {
#         'post': post,
#         'menu': menu,
#         'title': post.title,
#         'cat_selected': post.cat_id,
#     }
#
#     return render(request, 'women/post.html', context=context)

class WomenCategory(DataMixin,ListView):
    model = Women
    template_name = 'women/index.html'#по умолчанию будет искаться в имя приложения/имя модели_list.html
    context_object_name = 'posts'# по умолчанию называется object_list
    allow_empty = False# если нет ни одной записи то генерируется 404

    def get_queryset(self):#будем публиковать только с тру
        return Women.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True).select_related('cat')
        # cat__slug обрщаемся к cat связанной с моделью у которой есть slug

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)#что не затереть уже созданный уже контекст
        #context['menu'] = menu
        #context['title'] = 'Категория - ' + str(context['posts'][0].cat)
        #context['cat_selected'] = context['posts'][0].cat_id
        c = Category.objects.get(slug=self.kwargs['cat_slug'])
        c_def = self.get_user_context(title='Категория - ' + str(c.name), cat_selected=c.pk)
        return dict(list(context.items()) + list(c_def.items()))

# def show_category(request, cat_slug):
#     cat = Category.objects.filter(slug=cat_slug)
#     posts = Women.objects.filter(cat_id=cat[0].id)
#
#     if len(posts) == 0:
#         raise Http404()
#
#     context = {
#         'posts': posts,
#         'menu': menu,
#         'title': 'Отображение по ...',
#         'cat_selected': cat[0].id
#     }
#     return render(request, 'women/index.html', context=context)


def archive(request, year):
    if int(year) > 2023:
        #return redirect('/') адрес поменялся временно 302
        return redirect('home', permanent=True) #301, перенаправляет на другую стр
        #raise Http404()
    return HttpResponse(f"<h1>Архив по годам</h1><p>{year}</p>")


def pageNotFound(request, exception):
    return HttpResponseNotFound(f"<h1>Страница не найдена</h1>")


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'women/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)#что не затереть уже созданный уже контекст
        c_def = self.get_user_context(title='Регистрация')
        return dict(list(context.items()) + list(c_def.items()))

    def from_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'women/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)#что не затереть уже созданный уже контекст
        c_def = self.get_user_context(title='Авторизация')
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('home')


def logout_user(request):
    logout(request)
    return redirect('login')

#API
from rest_framework.views import APIView

# class WomenAPIView(generics.ListAPIView):
#     queryset = Women.objects.all()
#     serializer_class = WomenSerializer

class WomenAPIView(APIView):

    def get(self, request):
        w = Women.objects.all()
        return Response({'posts': WomenSerializer(w, many=True).data})
        #many=True - что будет обрабатывать много записей
        #Response - переводит в байтовую строку

    def post(self, request):
        serializer = WomenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        #формируется словарь valided data и этот словарь передается потом в сериализатор
        # чтобы при ошибке у нас все равно возвращалась json строка, а не страница с ошибкой
        serializer.save()
        #автоматичсеки будет вызвана create и будет добавлена запись

        return Response({'post':serializer.data})
    # many по умолчанию false

    def put(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        if not pk:
            return Response({'error': 'Method PUT not allowed'})

        
