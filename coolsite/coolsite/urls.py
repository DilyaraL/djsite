"""coolsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from coolsite import settings
from women.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/womenlist/', WomenAPIView.as_view()),
    path('captcha/', include('captcha.urls')),
    path('', include('women.urls')),

]

# это делается только в отладочном режиме, на реальных серверах это как правило настроено
if settings.DEBUG:
    import debug_toolbar #вне дебага он работать и не будет
    urlpatterns = [
                      path('__debug__/', include(debug_toolbar.urls)),
                  ] + urlpatterns
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = pageNotFound # обработчику 404 указали использовать нашу функцию для не сущ. страниц,
# она будет всегда вызываться при 404. Есть и другие обработчики, все они работют при DEBUG=False