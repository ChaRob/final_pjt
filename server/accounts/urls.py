from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

app_name='accounts'

urlpatterns = [
    path('userinfo/<int:user_pk>/', views.userinfo),
    path('update/', views.update, name='update'),
    path('follow/<int:user_pk>/', views.follow, name='follow'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

