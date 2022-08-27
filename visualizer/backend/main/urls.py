from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.home),
    path('tiles/<int:z>/<int:x>/<int:y>.png', views.tile),
]
