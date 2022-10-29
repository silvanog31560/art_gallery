from django.urls import path

from . import views

app_name='reviews'
urlpatterns = [
    path('', views.ReviewListview.as_view(), name="reviews-list"),
    path('create-review', views.ReviewCreate.as_view(), name="create-review"),
    path('edit-review/<int:pk>', views.ReviewUpdate.as_view(), name="edit-review"),
    path('delete-review/<int:pk>', views.ReviewDelete.as_view(), name="delete-review"),
]
