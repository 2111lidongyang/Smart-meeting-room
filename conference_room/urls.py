from django.urls import path
from . import views as conference_views

urlpatterns = [
    path('login/', conference_views.conference_home),
    path('manager_login/', conference_views.conference_manager_login),
    path('compere_login/', conference_views.conference_compere_login),
    path('manager_register/', conference_views.manager_register),
    path('upload_image/', conference_views.upload_image, name='upload_image'),
]
