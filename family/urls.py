from django.urls import path
from .views import *

urlpatterns = [
    path('new/', new, name="new_f"),
    path('detail/<int:pk>', detail, name="detail_f"),
    path('detail/edit/<int:pk>', edit, name="edit_f"),
    path('detail/delete/<int:pk>', delete, name="delete_f"),
]