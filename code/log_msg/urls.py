from django.urls import path

from . import views
from .models import LogMessage

home_list_view = views.HomeListView.as_view(
    queryset=LogMessage.objects.order_by('-log_date')[:5],
    context_object_name='message_list',
    template_name='log_msg/home.html',
)

urlpatterns = [
    path('log/', views.log_message, name='log'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('', home_list_view, name='home'),
]
