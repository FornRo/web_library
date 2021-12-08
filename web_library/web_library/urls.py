from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('catalog/', include(('catalog.urls', 'catalog'))),

]

#  static_file
from django.conf import settings
from django.conf.urls.static import static


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


from django.views.generic import RedirectView
urlpatterns += [
    path('', RedirectView.as_view(url='/catalog/', permanent=True)),
]