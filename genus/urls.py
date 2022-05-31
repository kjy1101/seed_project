from django.urls import path
from .views import *

urlpatterns = [
    path('new/', new, name="new_g"),
    path('detail/<int:pk>', detail, name="detail_g"),
    path('detail/edit/<int:pk>', edit, name="edit_g"),
    path('detail/delete/<int:pk>', delete, name="delete_g"),
]