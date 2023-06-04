from django.db import models
from django.urls import reverse


class Women(models.Model): #models.Model базовый класс, кот. содержит все необходимые механизмы,
    # чтобы мы создали свои классы-модели
    # id прописано уже в Модел
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    content = models.TextField(blank=True, verbose_name='Текст статьи')
    photo = models.ImageField(upload_to="photos/%Y/%m/%d", verbose_name='Фото') #в какой под каталог будем грузить фото
    #чтобы джанго автоматичсеки загружал фото и формировал путь, надо настроить константы MEDIA_ROOT, MEDIA_URL
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')#добавит в поле текущее время и больше никогла меняться не будет
    time_update = models.DateTimeField(auto_now=True, verbose_name='Время изменения')
    is_published = models.BooleanField(default=True, verbose_name='Публикация')
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name='Категории')# джанго автоматиски добавит в имя _id

    def __str__(self):
        return self.title


    def get_absolute_url(self): #будем формирать маршрут
        return reverse('post', kwargs={'post_slug': self.slug})

    class Meta:
        verbose_name = 'Известные женщины'
        verbose_name_plural = 'Известные женщины'
        ordering = ['-time_create', 'title'] #сортировка в обратном порядке


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name='Категория')# поле будет проидексировано
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")

    def __str__(self):
        return self.name

    def get_absolute_url(self): #будем формирать маршрут
        return reverse('category', kwargs={'cat_slug': self.slug})

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
