from django.urls import path
from .views import *

urlpatterns = [
    path('new/', new, name="new"),
    path('detail/<int:pk>', detail, name="detail"),
    path('detail/edit/<int:pk>', edit, name="edit"),
    path('detail/delete/<int:pk>', delete, name="delete"),
]