from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.index, name='home'),
    path('login', views.loginPage, name='login'),
    path('logout', views.logoutUser, name='logout'),
    path('register', views.RegisterPage, name='register'),
    path('create_organization', views.create_organization, name='create_organization'),
    path('services/<int:services_id>', views.services, name='services'),
    path('create_services', views.create_services, name='create_services'),
    path('report', views.report, name='report'),
    # path('create_adm/<int:id>', views.create_adm, name='create_adm'),
]# + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
