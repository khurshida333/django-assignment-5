from django.contrib import admin
from django.urls import path,include
from core.views import HomeView
from .import views
from core.views import index
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', index, name='home'),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('transactions/', include('transactions.urls')),
    path('categories/', include('categories.urls')),
    path('category/<slug:category_slug>/', index, name = 'category_wise_book'),
    path('books/', include('books.urls')),
]


urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
