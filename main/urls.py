from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.index, name='home'),

    # path('create_adm/<int:id>', views.create_adm, name='create_adm'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)