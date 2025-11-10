from django.urls import path

from door_visits import views

urlpatterns = [
    path('visits/', views.ewm_view),
    path('image/', views.image_view, name='image_view'),
    path('update/<str:username>', views.update_qr)

]
